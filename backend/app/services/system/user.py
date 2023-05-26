import typing
from datetime import datetime
import traceback
import uuid

from app.corelibs import g
from loguru import logger
from app.corelibs.codes import CodeEnum
from app.corelibs.consts import TEST_USER_INFO, CACHE_DAY
from app.models.system_models import User, Menu, Roles, UserLoginRecord
from app.schemas.system.user import UserLogin, UserIn, UserResetPwd, UserDel, UserQuery, \
    UserLoginRecordIn, UserLoginRecordQuery
from app.services.system.menu import MenuService
from app.utils.current_user import current_user
from app.utils.des import encrypt_rsa_password, decrypt_rsa_password
from app.corelibs.serialize import default_serialize


class UserService:
    """用户类"""

    @staticmethod
    async def login(params: UserLogin) -> typing.Dict[typing.Text, typing.Any]:
        """
        登录
        :return:
        """
        username = params.username
        password = params.password
        if not username and not password:
            raise ValueError(CodeEnum.PARTNER_CODE_PARAMS_FAIL.msg)
        user_info = await User.get_user_by_name(username)
        if not user_info:
            raise ValueError(CodeEnum.WRONG_USER_NAME_OR_PASSWORD.msg)
        u_password = decrypt_rsa_password(user_info["password"])

        if u_password != password:
            raise ValueError(CodeEnum.WRONG_USER_NAME_OR_PASSWORD.msg)
        token = str(uuid.uuid4())
        login_time = default_serialize(datetime.now())
        tags = user_info.get("tags", None)
        roles = user_info.get("roles", None)
        token_user_info = {
            "id": user_info["id"],
            "token": token,
            "login_time": login_time,
            "username": user_info["username"],
            "roles": roles if roles else [],
            "tags": tags if tags else []
        }
        await g.redis.set(TEST_USER_INFO.format(token), token_user_info, CACHE_DAY)
        logger.info('用户 [{}] 登录了系统'.format(user_info["username"]))

        try:
            login_ip = g.request.headers.get("X-Real-IP", None)
            if not login_ip:
                login_ip = g.request.client.host
            params = UserLoginRecordIn(
                token=token,
                code=user_info["username"],
                user_id=user_info["id"],
                user_name=user_info["nickname"],
                login_type="password",
                login_time=login_time,
                login_ip=login_ip,
            )
            await UserService.user_login_record(params)
        except Exception as err:
            logger.error(f"登录日志记录错误\n{err}")
        return token_user_info

    @staticmethod
    async def logout():
        """
        登出
        :return:
        """
        token = g.request.headers.get('token', None)
        try:
            await g.redis.delete(TEST_USER_INFO.format(token))
        except Exception as err:
            logger.error(traceback.format_exc())

    @staticmethod
    async def user_register(user_params: UserIn) -> "User":
        """用户注册"""
        user_info = await User.get_user_by_name(user_params.username)
        if user_info:
            raise ValueError(CodeEnum.USERNAME_OR_EMAIL_IS_REGISTER.msg)
        user = await User.create(**user_params.dict())
        return user

    @staticmethod
    async def list(params: UserQuery) -> typing.Dict[typing.Text, typing.Any]:
        """
        获取用户列表
        :param params:  查询参数
        :return:
        """
        data = await User.get_list(params)
        for row in data.get("rows"):
            roles = row.get("roles", None)
            tags = row.get("roles", None)
            row["roles"] = roles if roles else []
            row["tags"] = tags if tags else []
        return data

    @staticmethod
    async def save_or_update(params: UserIn) -> typing.Dict[typing.Text, typing.Any]:
        """
        用户保存方法
        :param params: 用户字段
        :return:
        """
        if not params.id:
            if User.get_user_by_name(params.nickname):
                raise ValueError('用户昵称已存在！')
        else:
            user_info = await User.get(params.id, to_dict=True)
            if user_info['nickname'] != params.nickname and User.get_user_by_nickname(params.nickname):
                raise ValueError('用户昵称已存在！')
        result = await User.create_or_update(params.dict())
        current_user_info = await current_user()
        if current_user_info.get("id") == params.id:
            token_user_info = {
                "id": result["id"],
                "token": current_user_info.get("token"),
                "login_time": current_user_info.get("login_time"),
                "username": result["username"],
                "roles": result["roles"],
                "tags": result["tags"]
            }
            await g.redis.set(TEST_USER_INFO.format(g.token), token_user_info, CACHE_DAY)
        return result

    @staticmethod
    async def deleted(params: UserDel):
        """
        删除用户
        :param params: 删除参数
        :return:
        """
        try:
            return await User.delete(params.id)
        except Exception as err:
            logger.error(traceback.format_exc())

    @staticmethod
    async def check_token(token: str) -> typing.Dict[typing.Text, typing.Any]:
        """
        校验token
        :param token: token
        :return:
        """
        user_info = await g.redis.get(TEST_USER_INFO.format(token))
        if not user_info:
            raise ValueError(CodeEnum.PARTNER_CODE_TOKEN_EXPIRED_FAIL.msg)

        user_info = {
            'id': user_info.get('id', None),
            'username': user_info.get('username', None)
        }
        return user_info

    @staticmethod
    async def reset_password(params: UserResetPwd):
        """修改密码"""

        if params.new_pwd != params.re_new_pwd:
            raise ValueError(CodeEnum.PASSWORD_TWICE_IS_NOT_AGREEMENT.msg)
        user_info = await User.get(params.id)
        pwd = decrypt_rsa_password(user_info.password)
        if params.old_pwd != pwd:
            raise ValueError(CodeEnum.OLD_PASSWORD_ERROR.msg)
        if params.new_pwd == pwd:
            raise ValueError(CodeEnum.NEW_PWD_NO_OLD_PWD_EQUAL.msg)
        new_pwd = encrypt_rsa_password(params.new_pwd)
        await User.update(**{"password": new_pwd, "id": params.id})

    @staticmethod
    async def get_user_info_by_token(token: str) -> typing.Union[typing.Dict[typing.Text, typing.Any], None]:
        """根据token获取用户信息"""
        token_user_info = await g.redis.get(TEST_USER_INFO.format(token))
        if not token_user_info:
            raise ValueError(CodeEnum.PARTNER_CODE_TOKEN_EXPIRED_FAIL.msg)
        user_info = await User.get(token_user_info.get("id"))
        if not user_info:
            raise ValueError(CodeEnum.PARTNER_CODE_TOKEN_EXPIRED_FAIL.msg)
        return {
            "id": user_info.id,
            "avatar": user_info.avatar,
            "username": user_info.username,
            "nickname": user_info.nickname,
            "roles": user_info.roles,
            "tags": user_info.tags,
            "login_time": token_user_info.get("login_time", None)
        }

    @staticmethod
    async def get_menu_by_token(token: str) -> typing.List[typing.Dict[typing.Text, typing.Any]]:
        """菜单权限"""
        current_user_info = await current_user(token)
        if not current_user_info:
            return []
        user_info = await User.get(current_user_info.get("id"))
        if not user_info or not user_info.roles:
            return []
        menu_ids = []
        if user_info.user_type == 10:
            all_menu = await Menu.get_menu_all()
            menu_ids += [i["id"] for i in all_menu]
        else:
            roles = await Roles.get_roles_by_ids(user_info.roles if user_info.roles else [])
            for i in roles:
                menu_ids += list(map(int, i["menus"].split(',')))
            if not menu_ids:
                return []
            parent_menus = await Menu.get_parent_id_by_ids(list(set(menu_ids)))
            # 前端角色报错只保存子节点数据，所有这里要做处理，把父级菜单也返回给前端
            menu_ids += [i["parent_id"] for i in parent_menus]
            all_menu = await Menu.get_menu_by_ids(list(set(menu_ids)))
        parent_menu = [menu for menu in all_menu if menu['parent_id'] == 0]
        return MenuService.menu_assembly(parent_menu, all_menu) if menu_ids else []

    @staticmethod
    async def user_login_record(params: UserLoginRecordIn):
        result = await UserLoginRecord.create_or_update(params.dict())
        return result


class LoginRecordService:
    @staticmethod
    async def list(params: UserLoginRecordQuery) -> typing.Dict[typing.Text, typing.Any]:
        """
        获取用户列表
        :param params:  查询参数
        :return:
        """
        data = await UserLoginRecord.get_list(params)
        for row in data.get("rows"):
            if not row["roles"]:
                row["roles"] = []
            else:
                row["roles"] = list(map(int, row["roles"].split(',')))
        return data

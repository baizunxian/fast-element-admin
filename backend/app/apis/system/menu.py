from app.corelibs.custom_router import APIRouter
from app.utils.response import HttpResponse
from app.schemas.system.menu import MenuIn, MenuDel, MenuViews
from app.services.system.menu import MenuService

router = APIRouter()


@router.post('/allMenu', description="获取所有菜单数据")
async def all_menu():
    data = await MenuService.all_menu()
    return await HttpResponse.success(data)


@router.post('/getAllMenus', description="获取菜单嵌套结构")
async def get_all_menus():
    data = await MenuService.all_menu_nesting()
    return await HttpResponse.success(data)


@router.post('/saveOrUpdate', description="新增或者更新menu")
async def save_or_update(params: MenuIn):
    # return await HttpResponse.success(code=codes.PARTNER_CODE_FAIL, msg="演示环境不保存！")
    await MenuService.save_or_update(params)
    return await HttpResponse.success()


@router.post('/deleted', description="删除菜单")
async def delete_menu(params: MenuDel):
    data = await MenuService.deleted(params)
    return await HttpResponse.success(data)


@router.post('/setMenuViews', description="设置菜单访问量")
async def set_menu_views(params: MenuViews):
    await MenuService.set_menu_views(params)
    return await HttpResponse.success()

<template>
  <div class="personal layout-pd">
    <el-row>
      <!-- 个人信息 -->
      <el-col :xs="24" :sm="8" style="padding: 0 10px">
        <z-card>
          <div class="personal-user">
            <div class="personal-user-avatar" @click="onCropperDialogOpen">

              <el-avatar :size="100"
                         :src="state.userInfoForm.avatar"
                         title="点击更换头像"
                         :style="state.userInfoForm.avatar? {'--el-avatar-bg-color': 'transparent'}: {}"
                         style="cursor: pointer; ">
                <span style="font-size: 40px">{{
                    state.userInfoForm?.nickname ? state.userInfoForm?.nickname.slice(0, 1).toUpperCase() : ""
                  }}</span>
              </el-avatar>

            </div>
            <div class="personal-user-right">
              <el-row>
                <el-col :span="24">
                  <div class="personal-user-name">
                    <strong>{{ state.userInfoForm.nickname }}</strong>
                  </div>
                </el-col>
                <el-col :span="24">
                  <div class="personal-user-description">
                    <div>
                      <span>{{ state.userInfoForm.remarks }}</span>
                    </div>
                  </div>
                </el-col>

                <el-col :span="24">
                  <el-divider content-position="left">个人信息</el-divider>
                </el-col>
                <el-col :span="24">
                  <div class="personal-item">
                    <div class="personal-item-label">昵称：</div>
                    <div class="personal-item-value">{{ userStores.userInfos.nickname }}</div>
                  </div>
                </el-col>

                <el-col :span="24">
                  <div class="personal-item">
                    <div class="personal-item-label">身份：</div>
                    <div class="personal-item-value">超级管理</div>
                  </div>
                </el-col>

                <el-col :span="24">
                  <div class="personal-item">
                    <div class="personal-item-label">登录IP：</div>
                    <div class="personal-item-value">192.168.1.1</div>
                  </div>
                </el-col>

                <el-col :span="24">
                  <div class="personal-item">
                    <div class="personal-item-label">登录时间：</div>
                    <div class="personal-item-value">{{ userInfos.login_time }}</div>
                  </div>
                </el-col>

                <el-col :span="24">
                  <div class="personal-item">
                    <div class="personal-item-label">密码：</div>
                    <div class="personal-item-value">
                      <el-button text type="primary" @click="updatePassword">修改密码</el-button>
                    </div>
                  </div>
                </el-col>
                <el-col :span="24">
                  <el-button type="primary" @click="state.showEditPage = !state.showEditPage">
                    <el-icon>
                      <ele-Position/>
                    </el-icon>
                    更新个人信息
                  </el-button>
                </el-col>

                <el-col :span="24">
                  <el-divider content-position="left">个性标签</el-divider>
                </el-col>
                <el-col :span="24">
                  <div class="personal-item-tag">
                    <el-tag
                        v-for="tag in state.userInfoForm.tags"
                        :key="tag"
                        size="default"
                        type="success"
                        style="{margin-left: 0.25rem;margin-right: 0.25rem;}"
                        :disable-transitions="false"
                    >{{ tag }}
                    </el-tag>
                  </div>
                </el-col>

              </el-row>
            </div>
          </div>
        </z-card>
      </el-col>

      <!-- 消息通知 -->
      <el-col :xs="24" :sm="16" class="pl15 personal-info">
        <z-card shadow="hover">
          <template #header>
            <span>消息通知</span>
          </template>
          <div class="personal-info-box">
            <ul class="personal-info-ul">
              <li v-for="(v, k) in state.newsInfoList" :key="k" class="personal-info-li">
                <a :href="v.link" target="_block" class="personal-info-li-title">{{ v.title }}</a>
              </li>
            </ul>
          </div>
        </z-card>
      </el-col>


    </el-row>
    <!-- 更新信息 -->
    <el-dialog title="更新"
               destroy-on-close
               v-model="state.showEditPage">
      <el-row>
        <el-col :span="24" style="padding: 0 10px">
          <z-card class="personal-edit">
            <div class="personal-edit-title">基本信息</div>
            <el-form :model="state.userInfoForm" size="default" label-width="auto" class="mt35 mb35">
              <el-row :gutter="35">
                <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
                  <el-form-item label="昵称">
                    <el-input v-model="state.userInfoForm.nickname" placeholder="请输入昵称" clearable></el-input>
                  </el-form-item>
                </el-col>
                <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
                  <el-form-item label="签名">
                    <el-input v-model="state.userInfoForm.remarks" placeholder="请输入签名" clearable></el-input>
                  </el-form-item>
                </el-col>

                <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
                  <el-form-item label="个性标签">
                    <el-tag
                        v-for="tag in state.userInfoForm.tags"
                        :key="tag"
                        size="default"
                        type="success"
                        closable
                        style="{margin-left: 0.25rem;margin-right: 0.25rem;}"
                        :disable-transitions="false"
                        @close="removeTag(tag)"
                    >{{ tag }}
                    </el-tag>

                    <el-input
                        v-if="state.editTag"
                        ref="UserTagInputRef"
                        v-model="state.tagValue"
                        class="ml-1 w-20"
                        size="small"
                        @keyup.enter="addTag"
                        @blur="addTag"
                        style="width: 100px"
                    />
                    <el-button v-else size="small" @click="showEditTag">
                      + New Tag
                    </el-button>
                    <!--                  <el-input v-model="state.userInfoForm.tags" placeholder="请输入签名" clearable></el-input>-->
                  </el-form-item>
                </el-col>

                <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
                  <el-form-item label="邮箱">
                    <el-input v-model="state.userInfoForm.email" placeholder="请输入邮箱" clearable></el-input>
                  </el-form-item>
                </el-col>
              </el-row>
            </el-form>
          </z-card>
        </el-col>
      </el-row>
      <template #footer>
        <el-button type="primary" @click="save">
          更新
        </el-button>
      </template>
    </el-dialog>

    <SeePictures ref="SeePicturesRef" @updateAvatar="updateAvatar"></SeePictures>

    <ResetPassword ref="ResetPasswordRef"></ResetPassword>
  </div>
</template>

<script setup lang="ts" name="personal">
import {computed, defineAsyncComponent, nextTick, onMounted, reactive, ref} from 'vue';
import {formatAxis} from '/@/utils/formatTime';
import {useUserStore} from "/@/stores/user";
import {useUserApi} from "/@/api/useSystemApi/user";
import {ElMessage} from "element-plus";
import {storeToRefs} from "pinia";
import ResetPassword from "/@/views/system/personal/ResetPassword.vue";

const SeePictures = defineAsyncComponent(() => import("/@/components/seePictures/index.vue"))
const SeePicturesRef = ref();
const UserTagInputRef = ref();
const ResetPasswordRef = ref();
// 用户信息
const userStores = useUserStore()
const {userInfos} = storeToRefs(userStores);


// 定义变量内容
const state = reactive({
  newsInfoList: [],
  recommendList: [],
  userInfoForm: {
    id: null,
    username: '',
    nickname: '',
    avatar: '',
    remarks: '',
    email: '',
    tags: [],
  } as any,
  editTag: false,
  tagValue: "",
  showEditPage: false,
  cropperImg: '',
});

const getUserInfo = async () => {
  console.log(userInfos.value, '---> userInfos')
  let {data} = await useUserApi().getUserInfo({id: userInfos.value.id})
  // if (!data.avatar) {
  //   data.avatar = "data:image/png;base64,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"
  // }
  state.userInfoForm = data
}

// 当前时间提示语
const currentTime = computed(() => {
  return formatAxis(new Date());
});

// 打开裁剪弹窗
const onCropperDialogOpen = () => {
  SeePicturesRef.value.openDialog(state.userInfoForm.avatar);
};


// tags
const showEditTag = () => {
  state.editTag = true
  nextTick(() => {
    UserTagInputRef.value?.input.focus()
  })
}

const removeTag = (tag) => {
  state.userInfoForm.tags.splice(state.userInfoForm.tags.indexOf(tag), 1)
}

const addTag = () => {
  if (state.editTag && state.tagValue) {
    if (!state.userInfoForm.tags) state.userInfoForm.tags = []
    state.userInfoForm.tags.push(state.tagValue)
  }
  state.editTag = false
  state.tagValue = ''
}

const save = async () => {
  let {data} = await useUserApi().saveOrUpdate(state.userInfoForm)
  ElMessage.success("更新成功!╰(*°▽°*)╯😍")
  state.showEditPage = false
}

const updateAvatar = async (img: string) => {
  state.userInfoForm.avatar = img
  await useUserApi().updateUserAvatar({id: state.userInfoForm.id, avatar: img})
  userInfos.value.avatar = img
  await userStores.updateUserInfo(userInfos.value)
  ElMessage.success("更新成功!╰(*°▽°*)╯😍")

}

const updatePassword = () => {
  ResetPasswordRef.value.openDialog(userInfos.value)
}

onMounted(() => {
  nextTick(() => {
    getUserInfo()
  })
})
</script>

<style scoped lang="scss">
@import '../../../theme/mixins/index.scss';

.personal {
  .personal-user {
    //height: 130px;
    //display: flex;
    align-items: center;
    padding: 20px;


    .personal-user-avatar {
      width: 100px;
      height: 100px;
      margin: auto;
      border-radius: 3px;
      margin-bottom: 20px;

      img {
        cursor: pointer;
        width: 100%;
        height: 100%;
        border-radius: 50%;
      }
    }


    .personal-user-right {
      flex: 1;
      padding: 0 15px;

      .personal-user-name {
        text-align: center;
        font-size: 20px;
        margin-bottom: 10px;
      }

      .personal-user-description {
        text-align: center;
      }

      .personal-title {
        font-size: 18px;
        @include text-ellipsis(1);
      }

      .personal-item {
        display: flex;
        align-items: center;
        font-size: 13px;
        height: 30px;
        width: 100%;
        flex-flow: wrap;

        .personal-item-label {
          color: var(--el-text-color-secondary);
          @include text-ellipsis(1);
        }

        .personal-item-value {
          @include text-ellipsis(1);
        }
      }

      .personal-item-tag {
        .personal-item-tag-item {
          margin: 5px;
          float: left;
        }
      }
    }
  }

  .personal-info {

    .personal-info-box {
      height: 130px;
      overflow: hidden;

      .personal-info-ul {
        list-style: none;

        .personal-info-li {
          font-size: 13px;
          padding-bottom: 10px;

          .personal-info-li-title {
            display: inline-block;
            @include text-ellipsis(1);
            color: var(--el-text-color-secondary);
            text-decoration: none;
          }

          & a:hover {
            color: var(--el-color-primary);
            cursor: pointer;
          }
        }
      }
    }
  }

  .personal-recommend-row {
    .personal-recommend-col {
      .personal-recommend {
        position: relative;
        height: 100px;
        border-radius: 3px;
        overflow: hidden;
        cursor: pointer;

        &:hover {
          i {
            right: 0px !important;
            bottom: 0px !important;
            transition: all ease 0.3s;
          }
        }

        i {
          position: absolute;
          right: -10px;
          bottom: -10px;
          font-size: 70px;
          transform: rotate(-30deg);
          transition: all ease 0.3s;
        }

        .personal-recommend-auto {
          padding: 15px;
          position: absolute;
          left: 0;
          top: 5%;
          color: var(--next-color-white);

          .personal-recommend-msg {
            font-size: 12px;
            margin-top: 10px;
          }
        }
      }
    }
  }

  .personal-edit {
    .personal-edit-title {
      position: relative;
      padding-left: 10px;
      color: var(--el-text-color-regular);

      &::after {
        content: '';
        width: 2px;
        height: 10px;
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        background: var(--el-color-primary);
      }
    }

    .personal-edit-safe-box {
      border-bottom: 1px solid var(--el-border-color-light, #ebeef5);
      padding: 15px 0;

      .personal-edit-safe-item {
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: space-between;

        .personal-edit-safe-item-left {
          flex: 1;
          overflow: hidden;

          .personal-edit-safe-item-left-label {
            color: var(--el-text-color-regular);
            margin-bottom: 5px;
          }

          .personal-edit-safe-item-left-value {
            color: var(--el-text-color-secondary);
            @include text-ellipsis(1);
            margin-right: 15px;
          }
        }
      }

      &:last-of-type {
        padding-bottom: 0;
        border-bottom: none;
      }
    }
  }
}
</style>

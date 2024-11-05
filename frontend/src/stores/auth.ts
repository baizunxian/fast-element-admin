import { defineStore } from "pinia";
import { useUserStore } from "/@/stores/user";
import { useUserApi } from "/@/api/useSystemApi/user";
import { Session } from "/@/utils/storage";
import { initBackEndControlRoutes } from "/@/router/backEnd";
import { resetAllStores } from "/@/stores/setup";

export const useAuthStore = defineStore("auth", () => {
	const userStore = useUserStore();


	async function Login(params: any) {
		const { data } = await useUserApi().signIn(params)
		const token = data?.token
		Session.set('token', token);
		await userStore.setUserInfos();
		await initBackEndControlRoutes();
	}

	async function Logout() {
		await useUserApi().logout();
		Session.clear();
		resetAllStores()
	}

	return {
		Login,
		Logout
	}

})
import {defineStore} from 'pinia';

/**
 * 路由缓存列表
 * @methods setCacheKeepAlive 设置要缓存的路由 names（开启 Tagsview）
 * @methods addCachedView 添加要缓存的路由 names（关闭 Tagsview）
 * @methods delCachedView 删除要缓存的路由 names（关闭 Tagsview）
 * @methods delOthersCachedViews 右键菜单`关闭其它`，删除要缓存的路由 names（关闭 Tagsview）
 * @methods delAllCachedViews 右键菜单`全部关闭`，删除要缓存的路由 names（关闭 Tagsview）
 */
export const useKeepALiveNames = defineStore('keepALiveNames', {
	state: (): KeepAliveNamesState => ({
		keepAliveNames: [],
		cachedViews: [],
	}),
	actions: {
		setCacheKeepAlive(data: Array<string>) {
			this.keepAliveNames = data;
		},
		updateCacheKeepAlive(name: string) {
			const index = this.keepAliveNames.indexOf(name);
			index == -1 && this.keepAliveNames.push(name);
		},

		async addCachedView(isKeepAlive: boolean, fullPath: string) {
			const index = this.cachedViews.indexOf(fullPath);
			if (isKeepAlive && index == -1) this.cachedViews?.push(fullPath);
		},
		async delCachedView(fullPath: string) {
			const index = this.cachedViews.indexOf(fullPath);
			index > -1 && this.cachedViews.splice(index, 1);
		},
		async delOthersCachedViews(view: any) {
			if (view.meta.isKeepAlive) this.cachedViews = [view.name];
			else this.cachedViews = [];
		},
		async delAllCachedViews() {
			this.cachedViews = [];
		},
	},
});
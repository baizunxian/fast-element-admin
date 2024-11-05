import {defineStore} from 'pinia';
import {useLookupApi} from "/@/api/useSystemApi/lookup"
import {Session} from "/@/utils/storage";

/**
 * 数据字典
 * @methods setLookup 设置数据字典
 * @methods setColumnsMenuHover 设置分栏布局菜单鼠标移入 boolean
 * @methods setColumnsNavHover 设置分栏布局最左侧导航鼠标移入 boolean
 */
export const useLookupStore = defineStore('lookupDict', {
	state: (): LookUpState => ({
		lookupDict: []
	}),
	actions: {
		async setLookup() {
			if (Session.get('lookupDict')) {
				// pass
			} else {
				let res = await useLookupApi().getAllLookup()
				Session.set("lookupDict", res.data)
			}
			this.lookupDict = Session.get('lookupDict')
		},
		getLookup() {
			if (Session.get('lookupDict')) {
				this.lookupDict = Session.get('lookupDict')
			}
			return this.lookupDict
		}
	},
});

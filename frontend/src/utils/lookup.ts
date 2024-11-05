import {useLookupStore} from "/@/stores/lookup";
import {storeToRefs} from "/@/stores";
/**
 * 返回数据字典
 * @param code 数据字典编码
 * @param lookup_code 数据字典值编码
 * @returns return 对应的字符串，否则返回原值
 */
export function formatLookup(code: any, lookup_code: string): string {
	const lookupStore = useLookupStore()
	const {lookupDict} = storeToRefs(lookupStore);

	let lookup = lookupDict.value[code]
	if (!lookup) return lookup_code;
	if (lookup[lookup_code]) return lookup[lookup_code];
	return lookup_code;
}
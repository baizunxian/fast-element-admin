// 通用函数
import useClipboard from 'vue-clipboard3';
import {ElMessage} from 'element-plus';
import {formatDate} from '/@/utils/formatTime';
import MersenneTwister from './mersenneTwister.js'


export const {toClipboard} = useClipboard();

// 百分比格式化
export const percentFormat = (row: EmptyArrayType, column: number, cellValue: string) => {
	return cellValue ? `${cellValue}%` : '-';
};


// 列表日期时间格式化
export const dateFormatYMD = (row: EmptyArrayType, column: number, cellValue: string) => {
	if (!cellValue) return '-';
	return formatDate(new Date(cellValue), 'YYYY-mm-dd');
};
// 列表日期时间格式化
export const dateFormatYMDHMS = (row: EmptyArrayType, column: number, cellValue: string) => {
	if (!cellValue) return '-';
	return formatDate(new Date(cellValue), 'YYYY-mm-dd HH:MM:SS');
};
// 列表日期时间格式化
export const dateFormatHMS = (row: EmptyArrayType, column: number, cellValue: string) => {
	if (!cellValue) return '-';
	let time = 0;
	if (typeof row === 'number') time = row;
	if (typeof cellValue === 'number') time = cellValue;
	return formatDate(new Date(time * 1000), 'HH:MM:SS');
};
// 小数格式化
export const scaleFormat = (value: string = '0', scale: number = 4) => {
	return Number.parseFloat(value).toFixed(scale);
};
// 小数格式化
export const scale2Format = (value: string = '0') => {
	return Number.parseFloat(value).toFixed(2);
};
// 点击复制文本
export const copyText = (text: string, message?: string | null) => {
	return new Promise((resolve, reject) => {
		try {
			// 复制
			toClipboard(text);
			// 下面可以设置复制成功的提示框等操作
			ElMessage.success(message || '复制成功!');
			resolve(text);
		} catch (e) {
			// 复制失败
			ElMessage.error('复制失败!');
			reject(e);
		}
	});
};

export const getUuid = () => {
	return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
		var r = (Math.random() * 16) | 0,
			v = c == 'x' ? r : (r & 0x3) | 0x8;
		return v.toString(16);
	});
};


// 根据内容生成颜色
export const generateColorByContent = (str: string) => {
	let hash = 0
	for (let i = 0; i < str.length; i++) {
		hash = str.charCodeAt(i) + ((hash << 5) - hash)
	}
	// 这里使用伪随机数的原因是因为
	// 1. 如果字符串的内容差不多，根据hash生产的颜色就比较相近，不好区分，比如v1.1 v1.2，所以需要加入随机数来使得颜色能够区分开
	// 2. 普通的随机数每次数值不一样，就会导致每次新增标签原来的标签颜色就会发生改变，所以加入了这个方法，使得内容不变随机数也不变
	const rng = new MersenneTwister(hash)
	const h = rng.genrand_int32() % 360
	return 'hsla(' + h + ', 50%, 50%, 1)'
}

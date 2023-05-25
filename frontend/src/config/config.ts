//自动化平台后端域名

let url = null
let webSocketUri = null

export const getEnv = () => {
  if (window.location.href.includes('xxxxx.com') || window.location.href.includes('xx.xx.xx.xx')) return 'prd'     //prd
  return 'dev'                                                 //本地环境
}

const env = getEnv()

export const initConfig = () => {
  if (env === 'prd') {
    url = 'https://xxxxx.com:8888'
  } else {
    url = 'http://localhost:8102'
  }
}

initConfig()

export const BaseUrl = url + '/api'
const WebSocketUrl = ((window.location.protocol === 'https:') ? 'wss' : 'wss') + '://' + webSocketUri + '/ws/message'
export default {
  BaseUrl,
  env,
  WebSocketUrl,
}
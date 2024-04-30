/*
 * @Description: 
 * @Author: lyq
 * @Date: 2024-01-06 19:29:11
 * @LastEditTime: 2024-01-07 11:15:52
 * @LastEditors: lyq
 */
function generateUniqueString() {
      const timestamp = Date.now().toString(36); // 转为36进制以缩短长度
      const randomPart = Math.random().toString(36).substring(2, 10); // 获取一个小数部分的随机字符串
      return `${timestamp}-${randomPart}`;
    }


    var t=generateUniqueString();
    console.log(t);
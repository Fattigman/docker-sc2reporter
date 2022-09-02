import { default as axios } from 'axios'
import { Login } from './interfaces'
import { notification } from 'antd'

export const { REACT_APP_BACKEND_URL } = process.env

export const getToken = async (formInput: Login): Promise<any> => {
  const endPoint = `${REACT_APP_BACKEND_URL}/login/token`
  return new Promise((resolve, reject) => {
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore
    const params = new URLSearchParams(formInput)
    axios
      .post(endPoint, params, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      })
      .then((response) => resolve(response.data))
      .catch((error) => {
        console.log(error)
        notification.error({
          message: 'Something went wrong',
          description: 'Try again',
        })
      })
  })
}

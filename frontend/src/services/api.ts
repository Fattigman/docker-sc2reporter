import { default as axios } from 'axios'
import { notification } from 'antd'

export const { REACT_APP_BACKEND_URL } = process.env

export const getToken = async (formInput): Promise<any> => {
  const endPoint = `${REACT_APP_BACKEND_URL}/login/token`
  return new Promise((resolve) => {
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

export const getSamples = async (token): Promise<any> => {
  const endPoint = `${REACT_APP_BACKEND_URL}/samples`
  return new Promise((resolve) => {
    axios
      .get(endPoint, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((response) => resolve(response.data))
      .catch((error) => {
        console.log(error)
        notification.error({
          message: 'Could not load samples',
          description: 'Something went wrong',
        })
      })
  })
}

export const getNextclade = async (token, nextclade): Promise<any> => {
  const endPoint = `${REACT_APP_BACKEND_URL}/samples/nextclade/?nextclade=${nextclade}`
  return new Promise((resolve) => {
    axios
      .get(endPoint, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((response) => resolve(response.data))
      .catch((error) => {
        console.log(error)
        notification.error({
          message: 'Could not load Nextclade info',
          description: 'Something went wrong',
        })
      })
  })
}

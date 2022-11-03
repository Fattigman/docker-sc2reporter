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

export const getPangolin = async (token, pangolin): Promise<any> => {
  const endPoint = `${REACT_APP_BACKEND_URL}/samples/pango/?pangolin=${pangolin}`
  return new Promise((resolve) => {
    axios
      .get(endPoint, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((response) => resolve(response.data))
      .catch((error) => {
        console.log(error)
        notification.error({
          message: 'Could not load pangolin info',
          description: 'Something went wrong',
        })
      })
  })
}

export const getVariant = async (token, variant): Promise<any> => {
  const endPoint = `${REACT_APP_BACKEND_URL}/variants/${variant}`
  return new Promise((resolve) => {
    axios
      .get(endPoint, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((response) => resolve(response.data))
      .catch((error) => {
        console.log(error)
        notification.error({
          message: 'Could not load variant info',
          description: 'Something went wrong',
        })
      })
  })
}

export const getDashboard = async (token): Promise<any> => {
  const endPoint = `${REACT_APP_BACKEND_URL}/dashboard`
  return new Promise((resolve) => {
    axios
      .get(endPoint, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((response) => resolve(response.data))
      .catch((error) => {
        console.log(error)
        notification.error({
          message: 'Could not load dashboard info',
          description: 'Something went wrong',
        })
      })
  })
}

export const getSample = async (token, id): Promise<any> => {
  const endPoint = `${REACT_APP_BACKEND_URL}/samples/${id}`
  return new Promise((resolve) => {
    axios
      .get(endPoint, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((response) => resolve(response.data))
      .catch((error) => {
        console.log(error)
        notification.error({
          message: 'Could not load sample info',
          description: 'Something went wrong',
        })
      })
  })
}

export const getUsers = async (token): Promise<any> => {
  const endPoint = `${REACT_APP_BACKEND_URL}/users/`
  return new Promise((resolve) => {
    axios
      .get(endPoint, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((response) => resolve(response.data))
      .catch((error) => {
        console.log(error)
        notification.error({
          message: 'Could not load user list',
          description: error.response.data.detail,
        })
      })
  })
}

export const getUserInfo = async (token): Promise<any> => {
  const endPoint = `${REACT_APP_BACKEND_URL}/users/me`
  return new Promise((resolve) => {
    axios
      .get(endPoint, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((response) => resolve(response.data))
      .catch((error) => {
        console.log(error)
        notification.error({
          message: 'Could not load user info and scope',
          description: 'Something went wrong',
        })
      })
  })
}

export const addUser = async (token, formInput): Promise<any> => {
  const endPoint = `${REACT_APP_BACKEND_URL}/users/add`
  return new Promise((resolve) => {
    axios
      .post(endPoint, formInput, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((response) => resolve(response.data))
      .catch((error) => {
        console.log(error)
        notification.error({
          message: 'Could not add user',
          description: 'Something went wrong',
        })
      })
  })
}

export const deleteUser = async (token, username): Promise<any> => {
  const endPoint = `${REACT_APP_BACKEND_URL}/users/delete/?user=${username}`
  return new Promise((resolve) => {
    axios
      .delete(endPoint, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((response) => resolve(response.data))
      .catch((error) => {
        console.log(error)
        notification.error({
          message: 'Could not add user',
          description: 'Something went wrong',
        })
      })
  })
}

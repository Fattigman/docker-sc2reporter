import { default as axios } from 'axios'
import { notification } from 'antd'
import { handleBackendError } from 'helpers'

export const { REACT_APP_BACKEND_URL } = process.env

export const getToken = async (formInput): Promise<any> => {
  const endPoint = `${REACT_APP_BACKEND_URL}/login/token`
  return new Promise((resolve, reject) => {
    const params = new URLSearchParams(formInput)
    axios
      .post(endPoint, params, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      })
      .then((response) => resolve(response.data))
      .catch((error) => {
        handleBackendError(error)
        notification.error({
          message: error.response.statusText,
          description: error.response.data.message,
        })
        reject(error)
      })
  })
}

export const getSamples = async (token): Promise<any> => {
  const endPoint = `${REACT_APP_BACKEND_URL}/samples/`
  return new Promise((resolve, reject) => {
    axios
      .get(endPoint, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((response) => resolve(response.data))
      .catch((error) => {
        handleBackendError(error)
        notification.error({
          message: 'Could not load samples',
          description: 'Something went wrong',
        })
        reject(error)
      })
  })
}

export const getNextclade = async (token, nextclade): Promise<any> => {
  const endPoint = `${REACT_APP_BACKEND_URL}/samples/nextclade/?nextclade=${nextclade}`
  return new Promise((resolve, reject) => {
    axios
      .get(endPoint, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((response) => resolve(response.data))
      .catch((error) => {
        handleBackendError(error)
        notification.error({
          message: 'Could not load Nextclade info',
          description: 'Something went wrong',
        })
        reject(error)
      })
  })
}

export const getPangolin = async (token, pangolin): Promise<any> => {
  const endPoint = `${REACT_APP_BACKEND_URL}/samples/pango/?pangolin=${pangolin}`
  return new Promise((resolve, reject) => {
    axios
      .get(endPoint, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((response) => resolve(response.data))
      .catch((error) => {
        handleBackendError(error)
        notification.error({
          message: 'Could not load pangolin info',
          description: 'Something went wrong',
        })
        reject(error)
      })
  })
}

export const getVariant = async (token, variant): Promise<any> => {
  const endPoint = `${REACT_APP_BACKEND_URL}/samples/variant/?variant=${variant}`
  return new Promise((resolve, reject) => {
    axios
      .get(endPoint, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((response) => resolve(response.data))
      .catch((error) => {
        handleBackendError(error)
        notification.error({
          message: 'Could not load variant info',
          description: 'Something went wrong',
        })
        reject(error)
      })
  })
}

export const getDashboard = async (token, selectionCriterion): Promise<any> => {
  const endPoint = `${REACT_APP_BACKEND_URL}/dashboard/?${selectionCriterion}`
  return new Promise((resolve, reject) => {
    axios
      .get(endPoint, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((response) => resolve(response.data))
      .catch((error) => {
        handleBackendError(error)
        notification.error({
          message: 'Could not load dashboard info',
          description: 'Something went wrong',
        })
        reject(error)
      })
  })
}

export const getSample = async (token, id): Promise<any> => {
  const endPoint = `${REACT_APP_BACKEND_URL}/samples/${id}`
  return new Promise((resolve, reject) => {
    axios
      .get(endPoint, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((response) => resolve(response.data))
      .catch((error) => {
        handleBackendError(error)
        notification.error({
          message: 'Could not load sample info',
          description: 'Something went wrong',
        })
        reject(error)
      })
  })
}

export const deleteSample = async (token, sample_ids): Promise<any> => {
  const endPoint = `${REACT_APP_BACKEND_URL}/samples/?${sample_ids}`
  return new Promise((resolve, reject) => {
    axios
      .delete(endPoint, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((response) => resolve(response.data))
      .catch((error) => {
        handleBackendError(error)
        notification.error({
          message: 'Could not delete sample',
          description: 'Something went wrong',
        })
        reject(error)
      })
  })
}

export const getUsers = async (token): Promise<any> => {
  const endPoint = `${REACT_APP_BACKEND_URL}/users/`
  return new Promise((resolve, reject) => {
    axios
      .get(endPoint, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((response) => resolve(response.data))
      .catch((error) => {
        handleBackendError(error)
        notification.error({
          message: 'Could not load user list',
          description: error.response?.data?.detail,
        })
        reject(error)
      })
  })
}

export const getUserInfo = async (token): Promise<any> => {
  const endPoint = `${REACT_APP_BACKEND_URL}/users/me/`
  return new Promise((resolve, reject) => {
    axios
      .get(endPoint, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((response) => resolve(response.data))
      .catch((error) => {
        handleBackendError(error)
        notification.error({
          message: 'Could not load user info and scope',
          description: 'Something went wrong',
        })
        reject(error)
      })
  })
}

export const addUser = async (token, formInput): Promise<any> => {
  const endPoint = `${REACT_APP_BACKEND_URL}/users/add/`
  return new Promise((resolve, reject) => {
    axios
      .post(endPoint, formInput, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((response) => resolve(response.data))
      .catch((error) => {
        handleBackendError(error)
        notification.error({
          message: 'Could not add user',
          description: 'Something went wrong',
        })
        reject(error)
      })
  })
}

export const deleteUser = async (token, username): Promise<any> => {
  const endPoint = `${REACT_APP_BACKEND_URL}/users/delete/?user=${username}`
  return new Promise((resolve, reject) => {
    axios
      .delete(endPoint, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((response) => resolve(response.data))
      .catch((error) => {
        handleBackendError(error)
        notification.error({
          message: 'Could not delete user',
          description: 'Something went wrong',
        })
        reject(error)
      })
  })
}

export const getPhylogeny = async (token, group, samples): Promise<any> => {
  const endPoint = `${REACT_APP_BACKEND_URL}/phylogeny/?group=${group}&${samples}`
  return new Promise((resolve, reject) => {
    axios
      .get(endPoint, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((response) => resolve(response.data))
      .catch((error) => {
        handleBackendError(error)
        notification.error({
          message: 'Could not load phyllogeny info',
          description: 'Something went wrong',
        })
        reject(error)
      })
  })
}

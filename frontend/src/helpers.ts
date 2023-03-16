import moment from 'moment'

export const formatDate = (date: string) => (date ? moment(date).format('YYYY-MM-DD') : null)

export const sortDate = (dateA: string, dateB: string) => {
  return new Date(dateA).getTime() - new Date(dateB).getTime()
}

// Temporary function to decode HTML entities
export const decodeHTMLEntities = (array) => {
  const decodedArray: string[] = []
  array.map((str) => {
    const txt = document.createElement('textarea')
    txt.innerHTML = str
    decodedArray.push(txt.value)
  })
  return decodedArray
}

// Temporary function to encode a string for use in a URL
export function urlEncode(str) {
  let encodedStr = encodeURIComponent(str)
    .replace(/%C3%A4/g, '%26auml%3B') // encode "ä" as %26auml%3B
    .replace(/%C3%B6/g, '%26ouml%3B') // encode "ö" as %26ouml%3B
    .replace(/%C3%84/g, '%26Auml%3B') // encode "Ä" as %26Auml%3B
    .replace(/%C3%96/g, '%26Ouml%3B') // encode "Ö" as %26Ouml%3B
  encodedStr = encodedStr.replace(/%20/g, '%20') // replace spaces with %20
  return encodedStr
}

export const handleBackendError = (error) => {
  console.log(error)
  if (error?.response?.status === 404) {
    window.location.href = `/error`
  }
}

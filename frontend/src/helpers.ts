import moment from 'moment'

export const formatDate = (date: string) => (date ? moment(date).format('YYYY-MM-DD') : null)

export const sortDate = (dateA: string, dateB: string) => {
  return new Date(dateA).getTime() - new Date(dateB).getTime()
}

export const decodeHTMLEntities = (array) => {
  const decodedArray: string[] = []
  array.map((str) => {
    const txt = document.createElement('textarea')
    txt.innerHTML = str
    decodedArray.push(txt.value)
  })
  return decodedArray
}

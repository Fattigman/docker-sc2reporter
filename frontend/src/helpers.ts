import moment from 'moment'

export const formatDate = (date: string) => (date ? moment(date).format('YYYY-MM-DD') : null)

export const sortDate = (dateA: string, dateB: string) => {
  return new Date(dateA).getTime() - new Date(dateB).getTime()
}

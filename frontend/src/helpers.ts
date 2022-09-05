import moment from 'moment'

export const formatDate = (date: string) => (date ? moment(date).format('YYYY-MM-DD') : null)

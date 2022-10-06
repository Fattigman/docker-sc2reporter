import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { getNextclade } from '../services/api'
import { SamplesTable } from '../components/SamplesTable'
import { Card, PageHeader } from 'antd'

export const NextcladePage = ({ token }) => {
  const [samples, setSamples] = useState<any>()
  const { id } = useParams()

  useEffect(() => {
    if (id)
      getNextclade(token, id).then((response) => {
        setSamples(response)
      })
  }, [id])

  return (
    <Card>
      <PageHeader onBack={() => history.back()} title={'Nextclade'} />
      <SamplesTable samples={samples} />
    </Card>
  )
}

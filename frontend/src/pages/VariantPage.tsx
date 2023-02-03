import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { Card } from 'antd'
import { PageHeader } from '@ant-design/pro-layout'
import { getVariant } from '../services/api'
import { SamplesTable } from '../components/SamplesTable'

export const VariantPage = ({ token }) => {
  const [samples, setSamples] = useState<any>()
  const { id } = useParams()
  const title = `Variant ${id}`

  useEffect(() => {
    if (id)
      getVariant(token, id).then((response) => {
        setSamples(response)
      })
  }, [id])

  return (
    <Card>
      <PageHeader onBack={() => history.back()} title={title}>
        <SamplesTable samples={samples} />
      </PageHeader>
    </Card>
  )
}

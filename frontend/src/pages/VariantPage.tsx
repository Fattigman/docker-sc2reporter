import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { Card } from 'antd'
import { getVariant } from '../services/api'
import { SamplesTable } from '../components/SamplesTable'

export const VariantPage = ({ token }) => {
  const [samples, setSamples] = useState<any>()
  const { id } = useParams()

  useEffect(() => {
    if (id)
      getVariant(token, id).then((response) => {
        setSamples(response)
      })
  }, [id])

  return (
    <Card title={`Variant ${id}`}>
      <SamplesTable samples={samples} />
    </Card>
  )
}

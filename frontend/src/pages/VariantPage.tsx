import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { Card, Descriptions } from 'antd'
import { getVariant } from '../services/api'
import { PageHeader } from '@ant-design/pro-layout'
import { Loading } from 'components/Loading'

export const VariantPage = ({ token }) => {
  const [variant, setVariant] = useState<any>()
  const [isLoading, setIsLoading] = useState<boolean>(true)
  const { id } = useParams()
  const title = `Variant ${id}`

  useEffect(() => {
    if (id)
      getVariant(token, id).then((response) => {
        setVariant(response)
        setIsLoading(false)
      })
  }, [id])

  return isLoading ? (
    <Loading />
  ) : (
    <Card>
      <PageHeader onBack={() => history.back()} title={title}>
        <Descriptions bordered size="small" style={{ marginBottom: '40px' }}>
          <Descriptions.Item label="Genomics change">{variant}</Descriptions.Item>
          <Descriptions.Item label="Gene">{variant}</Descriptions.Item>
          <Descriptions.Item label="cDNA change">{variant}</Descriptions.Item>
          <Descriptions.Item label="Protein change">{variant}</Descriptions.Item>
          <Descriptions.Item label="Codon change">{variant}</Descriptions.Item>
          <Descriptions.Item label="Consequence">{variant}</Descriptions.Item>
          <Descriptions.Item label="External link: CoVariants">{variant}</Descriptions.Item>
        </Descriptions>
      </PageHeader>
    </Card>
  )
}

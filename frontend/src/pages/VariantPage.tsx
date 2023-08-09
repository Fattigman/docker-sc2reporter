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
        setVariant(response.variant_info[0].csq)
        setIsLoading(false)
      })
  }, [id])

  return isLoading ? (
    <Loading />
  ) : (
    <Card>
      <PageHeader onBack={() => history.back()} title={title}>
        <Descriptions bordered size="small" style={{ marginBottom: '40px' }}>
          <Descriptions.Item label="Gene">{variant.Gene}</Descriptions.Item>
          <Descriptions.Item label="cDNA change">{'----'}</Descriptions.Item>
          <Descriptions.Item label="Protein change">{'----'}</Descriptions.Item>
          <Descriptions.Item label="Codon change">{'----'}</Descriptions.Item>
          <Descriptions.Item label="Consequence">{variant.Consequence}</Descriptions.Item>
          <Descriptions.Item label="External link: CoVariants">{'----'}</Descriptions.Item>
        </Descriptions>
      </PageHeader>
    </Card>
  )
}

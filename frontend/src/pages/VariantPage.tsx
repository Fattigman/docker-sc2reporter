import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { Card, Descriptions } from 'antd'
import { getVariant } from '../services/api'
import { SamplesTable } from '../components/SamplesTable'
import { PageHeader } from '@ant-design/pro-layout'
import { Loading } from 'components/Loading'

export const VariantPage = ({ token, isAdmin }) => {
  const [samples, setSamples] = useState<any>()
  const [refresh, setRefresh] = useState<boolean>(false)
  const [isLoading, setIsLoading] = useState<boolean>(true)
  const { id } = useParams()
  const title = `Variant ${id}`

  useEffect(() => {
    if (id)
      getVariant(token, id).then((response) => {
        setSamples(response)
        setIsLoading(false)
      })
  }, [id, refresh])

  const refreshSamples = () => {
    setRefresh((prevRefresh) => !prevRefresh)
  }

  return isLoading ? (
    <Loading />
  ) : (
    <Card>
      <PageHeader onBack={() => history.back()} title={title}>
        <Descriptions bordered size="small" style={{ marginBottom: '40px' }}>
          <Descriptions.Item label="Genomics change">Genomics change</Descriptions.Item>
          <Descriptions.Item label="Gene">Gene</Descriptions.Item>
          <Descriptions.Item label="cDNA change">cDNA change</Descriptions.Item>
          <Descriptions.Item label="Protein change">Protein change</Descriptions.Item>
          <Descriptions.Item label="Codon change">Codon change</Descriptions.Item>
          <Descriptions.Item label="Consequence">Consequence</Descriptions.Item>
          <Descriptions.Item label="External link: CoVariants">
            External link: CoVariants
          </Descriptions.Item>
        </Descriptions>
        <SamplesTable
          token={token}
          samples={samples}
          refreshSamples={refreshSamples}
          isAdmin={isAdmin}
        />
      </PageHeader>
    </Card>
  )
}

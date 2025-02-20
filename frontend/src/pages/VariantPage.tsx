import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { Card, Descriptions, Space } from 'antd'
import { getVariant } from '../services/api'
import { PageHeader } from '@ant-design/pro-layout'
import { LoadingPage } from './LoadingPage'
import { SamplesTable } from 'components/SamplesTable'
import { LineGraphComponent } from 'components/LineGraphComponent'

export const VariantPage = ({ token, isAdmin }) => {
  const [variant, setVariant] = useState<any>()
  const [data, setData] = useState<any>()
  const [samples, setSamples] = useState<any>()
  const [refresh, setRefresh] = useState<boolean>(false)
  const [isLoading, setIsLoading] = useState<boolean>(true)
  const { id } = useParams()
  const title = `Variant ${id}`

  const refreshSamples = () => {
    setRefresh((prevRefresh) => !prevRefresh)
  }

  useEffect(() => {
    if (id)
      getVariant(token, id).then((response) => {
        setVariant(response.variant_info[0].csq)
        setData(response.graph)
        setSamples(response.samples)
        setIsLoading(false)
      })
  }, [id, refresh])

  return isLoading ? (
    <LoadingPage />
  ) : (
    <>
      <Card>
        <PageHeader onBack={() => history.back()} title={title}>
          <Space direction="vertical" size="large" style={{ display: 'flex' }}>
            <Descriptions bordered size="small">
              <Descriptions.Item label="Gene">{variant.Gene}</Descriptions.Item>
              <Descriptions.Item label="cDNA change">{variant.HGVSc}</Descriptions.Item>
              <Descriptions.Item label="Protein change">{variant.HGVSp}</Descriptions.Item>
              <Descriptions.Item label="Codon change">{variant.Codons}</Descriptions.Item>
              <Descriptions.Item label="Consequence">{variant.Consequence}</Descriptions.Item>
              <Descriptions.Item label="External link: CoVariants">{'----'}</Descriptions.Item>
            </Descriptions>
            <Card title={'Variant frequency over time'}>
              <LineGraphComponent data={data} />
            </Card>
            <Card>
              <SamplesTable
                token={token}
                samples={samples}
                refreshSamples={refreshSamples}
                isAdmin={isAdmin}
              />
            </Card>
          </Space>
        </PageHeader>
      </Card>
    </>
  )
}

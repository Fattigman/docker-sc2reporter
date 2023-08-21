import React, { useEffect, useState } from 'react'
import { Card, Space } from 'antd'
import { SamplesTable } from 'components/SamplesTable'
import { useParams } from 'react-router-dom'
import { getPangolin } from 'services/api'
import { PageHeader } from '@ant-design/pro-layout'
import { LoadingPage } from './LoadingPage'
import { LineGraphComponent } from 'components/LineGraphComponent'

export const PangolinPage = ({ token, isAdmin }) => {
  const [samples, setSamples] = useState<any>()
  const [data, setData] = useState<any>()
  const [refresh, setRefresh] = useState<boolean>(false)
  const [isLoading, setIsLoading] = useState<boolean>(true)
  const { id } = useParams()
  const title = `Pangolin ${id}`
  const covLineagesLink = `https://cov-lineages.org/lineage.html?lineage=${id}`

  const refreshSamples = () => {
    setRefresh((prevRefresh) => !prevRefresh)
  }

  useEffect(() => {
    if (id)
      getPangolin(token, id).then((response) => {
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
        <PageHeader
          onBack={() => history.back()}
          title={title}
          subTitle={<a href={covLineagesLink}>Lineage information</a>}
        >
          <Space direction="vertical" size="large" style={{ display: 'flex' }}>
            <Card title={'Pango type over time'}>
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

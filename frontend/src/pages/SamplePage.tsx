import React, { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { Card, Descriptions, PageHeader, Result, Tag } from 'antd'
import { CheckCircleTwoTone } from '@ant-design/icons'
import { formatDate } from '../helpers'
import { getSample } from '../services/api'
import { LoadingPage } from './LoadingPage'

export const SamplePage = ({ token }) => {
  const { id } = useParams()
  const [sample, setSample] = useState<any>()
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    setIsLoading(true)
    getSample(token, id).then((response) => {
      if (response?.[0]) setSample(response[0])
      setIsLoading(false)
    })
  }, [id])

  return isLoading ? (
    <LoadingPage />
  ) : sample.sample_id ? (
    <Card>
      <PageHeader onBack={() => history.back()} title={sample.sample_id}>
        <Descriptions bordered size="small">
          <Descriptions.Item label="Criterion">{sample.selection_criterion}</Descriptions.Item>
          <Descriptions.Item label="Date added">
            {formatDate(sample.time_added?.$date)}
          </Descriptions.Item>
          <Descriptions.Item label="Collection date">
            {formatDate(sample.collection_date?.$date)}
          </Descriptions.Item>
          <Descriptions.Item label="Pangolin">
            {sample.pangolin?.type != 'None' ? (
              <Link to={`/pangolin/${sample.pangolin?.type}`}>{sample.pangolin?.type}</Link>
            ) : (
              sample.pangolin?.type
            )}
          </Descriptions.Item>
          <Descriptions.Item label="Nextclade">
            <Link to={`/nextclade/${sample.nextclade}`}>{sample.nextclade}</Link>
          </Descriptions.Item>
          <Descriptions.Item label="Nr variants">{sample.variants?.length}</Descriptions.Item>
          <Descriptions.Item label="Similar samples">
            {sample.similar_samples?.map((sampleId) => (
              <>
                <Link to={`/samples/${sampleId}`} key={sampleId}>
                  {sampleId}
                </Link>
                <br />
              </>
            ))}
          </Descriptions.Item>
        </Descriptions>
        <br />
        <Descriptions
          title={
            <div>
              Quality control{' '}
              {sample.qc?.qc_pass === 'TRUE' ? (
                <CheckCircleTwoTone style={{ fontSize: 20 }} twoToneColor="#52c41a" />
              ) : (
                <Tag color={'volcano'}>FAIL</Tag>
              )}
            </div>
          }
          bordered
          size="small"
        >
          <Descriptions.Item label="Aligned reads">
            {sample.qc?.num_aligned_reads}
          </Descriptions.Item>
          <Descriptions.Item label="Reads on target">{sample.qc?.on_target}%</Descriptions.Item>
          <Descriptions.Item label="Covered in consensus seq">
            {sample.qc?.pct_covered_bases}%
          </Descriptions.Item>
          <Descriptions.Item label="Missing in consensus seq">
            {sample.qc?.pct_N_bases}%
          </Descriptions.Item>
        </Descriptions>
      </PageHeader>
    </Card>
  ) : (
    <Result status="404" title="404" subTitle="Sorry, the page you visited does not exist." />
  )
}

import React from 'react'
import { useParams } from 'react-router-dom'
import { Card, Descriptions, Result, Table, Tag } from 'antd'
import { CheckCircleTwoTone } from '@ant-design/icons'
import { formatDate } from '../helpers'

export const SamplePage = ({ samples }) => {
  const { id } = useParams()
  const sample = samples.filter((sample) => sample.sample_id === id)[0]

  return sample ? (
    <Card>
      <Descriptions title={sample.sample_id} bordered size="small">
        <Descriptions.Item label="Criterion">{sample.selection_criterion}</Descriptions.Item>
        <Descriptions.Item label="Date added">
          {formatDate(sample.time_added?.$date)}
        </Descriptions.Item>
        <Descriptions.Item label="Collection date">
          {formatDate(sample.collection_date?.$date)}
        </Descriptions.Item>
        <Descriptions.Item label="Pangolin">{sample.pangolin?.type}</Descriptions.Item>
        <Descriptions.Item label="Nextrain clade">{sample.nextclade}</Descriptions.Item>
        <Descriptions.Item label="Nr variants">{sample.variants?.length}</Descriptions.Item>
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
        <Descriptions.Item label="Aligned reads">{sample.qc?.num_aligned_reads}</Descriptions.Item>
        <Descriptions.Item label="Reads on target">{sample.qc?.on_target}%</Descriptions.Item>
        <Descriptions.Item label="Covered in consensus seq">
          {sample.qc?.pct_covered_bases}%
        </Descriptions.Item>
        <Descriptions.Item label="Missing in consensus seq">
          {sample.qc?.pct_N_bases}%
        </Descriptions.Item>
      </Descriptions>
    </Card>
  ) : (
    <Result status="404" title="404" subTitle="Sorry, the page you visited does not exist." />
  )
}

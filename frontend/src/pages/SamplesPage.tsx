import React from 'react'
import { Table, Tag } from 'antd'
import { formatDate, sortDate } from '../helpers'
import { CheckCircleTwoTone } from '@ant-design/icons'

export const SamplesPage = ({ samples }) => {
  const columns = [
    {
      title: 'ID',
      dataIndex: 'sample_id',
      key: 'sample_id',
      sorter: (a, b) => a.sample_id.localeCompare(b.title),
    },
    {
      title: 'Date added',
      dataIndex: 'time_added',
      key: 'time_added',
      render: (date) => formatDate(date?.$date),
      sorter: (a, b) => {
        console.log(a)
        return sortDate(a.time_added?.$date, b.time_added?.$date)
      },
    },
    {
      title: 'QC',
      dataIndex: 'qc',
      key: 'qc',
      render: (qc) =>
        qc?.qc_pass === 'TRUE' ? (
          <CheckCircleTwoTone twoToneColor="#52c41a" />
        ) : (
          <Tag color={'volcano'}>FAIL</Tag>
        ),
    },
    {
      title: 'Pangolin',
      dataIndex: 'pangolin',
      key: 'pangolin',
      render: (pangolin) => pangolin?.type,
    },
    {
      title: 'Significant variants',
      dataIndex: 'pangolin',
      key: 'pangolin',
      render: (pangolin) => pangolin?.type,
    },
    {
      title: 'Collection date',
      dataIndex: 'collection_date',
      key: 'collection_date',
      render: (date) => formatDate(date?.$date),
      sorter: (a, b) => sortDate(a.collection_date?.$date, b.collection_date?.$date),
    },
    {
      title: 'Criterion',
      dataIndex: 'selection_criterion',
      key: 'selection_criterion',
    },
  ]
  return (
    <Table
      pagination={false}
      dataSource={samples}
      columns={columns}
      key={'sample_id'}
      loading={!samples}
    />
  )
}

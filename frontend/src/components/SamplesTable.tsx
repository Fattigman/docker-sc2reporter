import React from 'react'
import { Table, Tag } from 'antd'
import { formatDate, sortDate } from '../helpers'
import { CheckCircleTwoTone } from '@ant-design/icons'
import { Link, useLocation } from 'react-router-dom'

export const SamplesTable = ({ samples }) => {
  const location = useLocation()

  const columns = [
    {
      title: 'ID',
      dataIndex: 'sample_id',
      key: 'sample_id',
      sorter: (a, b) => a.sample_id.localeCompare(b.title),
      render: (id) => <Link to={`/samples/${id}`}>{id}</Link>,
    },
    {
      title: 'Date added',
      dataIndex: 'time_added',
      key: 'time_added',
      render: (date) => formatDate(date?.$date),
      sorter: (a, b) => sortDate(a.time_added?.$date, b.time_added?.$date),
    },
    {
      title: 'QC',
      dataIndex: 'qc',
      key: 'qc',
      onFilter: (value, record) => record.qc?.qc_pass?.indexOf(value) === 0,
      filters: [
        {
          text: <Tag color={'volcano'}>FAIL</Tag>,
          value: 'FALSE',
        },
        {
          text: <CheckCircleTwoTone style={{ fontSize: 20 }} twoToneColor="#52c41a" />,
          value: 'TRUE',
        },
      ],
      render: (qc) =>
        qc?.qc_pass === 'TRUE' ? (
          <CheckCircleTwoTone style={{ fontSize: 20 }} twoToneColor="#52c41a" />
        ) : (
          <Tag color={'volcano'}>FAIL</Tag>
        ),
    },
    {
      title: 'Pangolin',
      dataIndex: 'pangolin',
      key: 'pangolin',
      render: (pangolin) =>
        pangolin?.type != 'None' ? (
          <Link to={`/pangolin/${pangolin?.type}`}>{pangolin?.type}</Link>
        ) : (
          pangolin?.type
        ),
      hidden: location?.pathname?.includes('pangolin'),
    },
    {
      title: 'Nextstrain clade',
      dataIndex: 'nextclade',
      key: 'nextclade',
      render: (nextclade) => <Link to={`/nextclade/${nextclade}`}>{nextclade}</Link>,
      hidden: location?.pathname?.includes('nextclade'),
    },
    {
      title: 'Significant variants',
      dataIndex: 'variants',
      key: 'variants',
      width: '40%',
      render: (variants) =>
        variants?.map((variant) => (
          <Tag color={'geekblue'} key={variant.id}>
            {variant.id}
          </Tag>
        )),
      ellipsis: true,
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
  ].filter((column) => !column.hidden)
  return (
    <>
      <Table
        pagination={false}
        dataSource={samples}
        columns={columns}
        rowKey={'sample_id'}
        loading={!samples}
      />
    </>
  )
}

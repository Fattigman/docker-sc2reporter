import React, { useEffect, useState } from 'react'
import { Button, Popconfirm, Table, Tag } from 'antd'
import { formatDate, sortDate } from '../helpers'
import { CheckCircleTwoTone, DeleteTwoTone } from '@ant-design/icons'
import { Link, useLocation } from 'react-router-dom'
import { deleteSample } from 'services/api'

export const SamplesTable = ({ token, samples }) => {
  const [selectedRowKeys, setSelectedRowKeys] = useState<any[]>([])
  const [samplesId, setSamplesId] = useState<string>('')
  const [sampleList, setSampleList] = useState<any[]>([])
  const location = useLocation()
  const nextclade = 'nextclade'
  const pangolin = 'pangolin'
  const hasSelected = selectedRowKeys.length > 0

  useEffect(() => {
    setSampleList(samples)
  }, [samples])

  const rowSelection = {
    onChange: (selectedRowKeys) => {
      setSelectedRowKeys(selectedRowKeys)
      const selectedSamples = selectedRowKeys.map((item) => `&sample_ids=${item}`).join('')
      setSamplesId(selectedSamples)
    },
    selectedRowKeys,
  }

  const confirmDelete = () => {
    deleteSample(token, samplesId).then(() => {
      setSampleList(sampleList.filter((sample) => !selectedRowKeys.includes(sample.sample_id)))
      setSelectedRowKeys([])
    })
  }

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
      hidden: location?.pathname?.includes(pangolin),
    },
    {
      title: 'Nextstrain clade',
      dataIndex: 'nextclade',
      key: 'nextclade',
      render: (nextclade) => <Link to={`/nextclade/${nextclade}`}>{nextclade}</Link>,
      hidden: location?.pathname?.includes(nextclade),
    },
    {
      title: 'Significant variants',
      dataIndex: 'variants',
      key: 'variants',
      width: '40%',
      render: (variants) =>
        variants?.map(({ id }) => (
          <Link key={id} to={`/variants/${id}`}>
            <Tag color={'geekblue'} key={id}>
              {id}
            </Tag>
          </Link>
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
        dataSource={sampleList}
        columns={columns}
        rowKey={'sample_id'}
        loading={!sampleList}
        rowSelection={{
          columnTitle: (
            <Popconfirm
              title="Are you sure you want to delete?"
              disabled={!hasSelected}
              onConfirm={confirmDelete}
            >
              <Button shape="circle" disabled={!hasSelected} icon={<DeleteTwoTone />} />
            </Popconfirm>
          ),
          ...rowSelection,
        }}
      />
    </>
  )
}

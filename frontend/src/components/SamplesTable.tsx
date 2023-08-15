import React, { useEffect, useState } from 'react'
import { Button, Card, Modal, notification, Popconfirm, Space, Table, Tag, Input } from 'antd'
import { formatDate, sortDate } from '../helpers'
import { CheckCircleTwoTone } from '@ant-design/icons'
import { Link, useLocation } from 'react-router-dom'
import { deleteSample, getPhylogeny } from 'services/api'

export const SamplesTable = ({ token, samples, refreshSamples, isAdmin }) => {
  const [selectedRowKeys, setSelectedRowKeys] = useState<any[]>([])
  const [samplesIds, setSamplesIds] = useState<string>('')
  const [filteredSamples, setFilteredSamples] = useState<any>('')
  const [copiedText, setCopiedText] = useState<string>('')
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false)
  const location = useLocation()
  const nextclade = 'nextclade'
  const pangolin = 'pangolin'
  const variants = 'variants'
  const group = 'samples'
  const hasSelected = selectedRowKeys.length > 0
  const { Search } = Input

  useEffect(() => {
    setFilteredSamples(samples)
  }, [samples])

  const onSearch = (value) => {
    const filtered = samples.filter((sample) =>
      sample.sample_id.toLowerCase().includes(value.toLowerCase())
    )
    setFilteredSamples(filtered)
  }

  const rowSelection = {
    onChange: (selectedRowKeys) => {
      setSelectedRowKeys(selectedRowKeys)
      const selectedSamplesIds = selectedRowKeys.map((item) => `sample_id=${item}`).join('&')
      setSamplesIds(selectedSamplesIds)
    },
    selectedRowKeys,
  }

  const confirmDelete = () => {
    deleteSample(token, samplesIds).then(() => {
      notification['success']({
        message:
          selectedRowKeys.length > 1
            ? `Samples (${selectedRowKeys}) have been successfully deleted.`
            : `Sample (${selectedRowKeys}) has been successfully deleted.`,
      })
      refreshSamples()
    })
  }

  const showModal = () => {
    setIsModalOpen(true)
  }

  const handleCancel = () => {
    setIsModalOpen(false)
  }

  const handleOk = () => {
    console.log(copiedText)
    navigator.clipboard.writeText(copiedText)
    setIsModalOpen(false)
    window.open('https://34.125.84.98/grapetree/')
    setSelectedRowKeys([])
  }

  const fetchPhylogenyData = async () => {
    if (selectedRowKeys.length > 2) {
      getPhylogeny(token, group, samplesIds).then((response) => {
        setCopiedText(JSON.stringify(response))
        if (response != '') {
          showModal()
          navigator.clipboard.writeText(JSON.stringify(response))
        }
      })
    } else {
      notification['info']({
        message:
          'To obtain Phylogeny data, you must select a minimum of three samples from the list provided below.',
        duration: 8,
      })
    }
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
      hidden: location?.pathname?.includes(variants),
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
    <Card>
      <Space direction="horizontal">
        <Button onClick={fetchPhylogenyData} type="primary">
          Fetch Phylogeny Data
        </Button>
        {isAdmin && (
          <Popconfirm
            title="Are you sure you want to delete?"
            disabled={!hasSelected}
            onConfirm={confirmDelete}
          >
            <Button disabled={!hasSelected} type="primary">
              Delete
            </Button>
          </Popconfirm>
        )}
      </Space>
      <Modal open={isModalOpen} onOk={handleOk} onCancel={handleCancel}>
        <p>
          The Phylogeny data has been successfully copied. Please click &apos;OK&apos; to go to the
          Grapetree site, then click on the &apos;Load files&apos; button and paste the data into
          the designated rectangle. Finally, click on the &apos;Confirm&apos; button to proceed.
        </p>
      </Modal>
      <div style={{ float: 'right' }}>
        <Search
          placeholder="Search by sample ID"
          onSearch={onSearch}
          enterButton
          allowClear
          style={{ width: '300px' }}
        />
      </div>
      <Table
        pagination={false}
        dataSource={filteredSamples}
        columns={columns}
        rowKey={'sample_id'}
        loading={!samples}
        bordered
        rowSelection={{
          ...rowSelection,
        }}
        style={{ marginTop: '30px' }}
      />
    </Card>
  )
}

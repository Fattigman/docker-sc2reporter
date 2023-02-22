import React, { useState } from 'react'
import { Button, Modal, notification, Popconfirm, Table, Tag } from 'antd'
import { PageHeader } from '@ant-design/pro-layout'
import { formatDate, sortDate } from '../helpers'
import { CheckCircleTwoTone } from '@ant-design/icons'
import { Link, useLocation } from 'react-router-dom'
import { deleteSample, getPhyllogeny } from 'services/api'
import styles from './SamplesTable.module.css'

export const SamplesTable = ({ token, samples, refreshSamples, isAdmin, title, subTitle }) => {
  const [selectedRowKeys, setSelectedRowKeys] = useState<any[]>([])
  const [samplesId, setSamplesId] = useState<string>('')
  const [samplesId2, setSamplesId2] = useState<string>('')
  const [copiedText, setCopiedText] = useState<string>('')
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false)
  const location = useLocation()
  const nextclade = 'nextclade'
  const pangolin = 'pangolin'
  const group = 'samples'
  const hasSelected = selectedRowKeys.length > 0

  const rowSelection = {
    onChange: (selectedRowKeys) => {
      setSelectedRowKeys(selectedRowKeys)
      const selectedSamples = selectedRowKeys.map((item) => `&sample_ids=${item}`).join('')
      const selectedSamples2 = selectedRowKeys.map((item) => `&sample_list=${item}`).join('')
      setSamplesId(selectedSamples)
      setSamplesId2(selectedSamples2)
    },
    selectedRowKeys,
  }

  const confirmDelete = () => {
    deleteSample(token, samplesId).then(() => {
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
    navigator.clipboard.writeText(copiedText)
    setIsModalOpen(false)
    window.open('https://34.125.84.98/grapetree/')
    setSelectedRowKeys([])
  }

  const fetchPhyllogenyData = async () => {
    if (selectedRowKeys.length > 2) {
      getPhyllogeny(token, group, samplesId2).then((response) => {
        setCopiedText(JSON.stringify(response))
        if (response != '') {
          showModal()
          navigator.clipboard.writeText(JSON.stringify(response))
        }
      })
    } else {
      notification['info']({
        message:
          'To obtain Phyllogeny data, you must select a minimum of three samples from the list provided below.',
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
      <PageHeader onBack={() => history.back()} title={title} subTitle={subTitle}>
        <Modal open={isModalOpen} onOk={handleOk} onCancel={handleCancel}>
          <p>
            The Phyllogeny data has been successfully copied. Please click &apos;OK&apos; to go to
            the Grapetree site, then click on the &apos;Load files&apos; button and paste the data
            into the designated rectangle. Finally, click on the &apos;Confirm&apos; button to
            proceed.
          </p>
        </Modal>
        <div className={styles.samplesTableButtons}>
          <Button onClick={fetchPhyllogenyData} type="primary">
            Fetch Phyllogeny Data
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
        </div>
        <Table
          pagination={false}
          dataSource={samples}
          columns={columns}
          rowKey={'sample_id'}
          loading={!samples}
          bordered
          rowSelection={{
            ...rowSelection,
          }}
        />
      </PageHeader>
    </>
  )
}

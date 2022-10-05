import { Card, Table, Tag, Typography } from 'antd'
import { formatDate, sortDate } from 'helpers'
import React, { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { getPangolin } from 'services/api'

export const PangolinPage = ({ token }) => {
  const [pangolin, setPangolin] = useState<any>()
  const { id } = useParams()
  const { Title } = Typography

  useEffect(() => {
    if (id)
      getPangolin(token, id).then((response) => {
        setPangolin(response)
      })
  }, [id])

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
      title: 'Nextstrain clade',
      dataIndex: 'nextclade',
      key: 'nextclade',
      render: (nextclade) => <Link to={`/nextclade/${nextclade}`}>{nextclade}</Link>,
    },
    {
      title: 'Significant mutations',
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
  ]

  return (
    <Card
      title={`Pangolin ${id}`}
      extra={
        <a href={`https://cov-lineages.org/lineage.html?lineage=${id}`}>Lineage information</a>
      }
    >
      <Table
        title={() => <Title level={5}>Samples</Title>}
        pagination={false}
        dataSource={pangolin}
        columns={columns}
        rowKey={'sample_id'}
        loading={!pangolin}
        style={{ margin: 20 }}
      />
    </Card>
  )
}

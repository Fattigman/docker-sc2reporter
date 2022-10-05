import React, { useEffect, useState } from 'react'
import { Card, Descriptions } from 'antd'
import { SamplesTable } from 'components/SamplesTable'
import { useParams } from 'react-router-dom'
import { getPangolin } from 'services/api'

export const PangolinPage = ({ token }) => {
  const [pangolin, setPangolin] = useState<any>()
  const { id } = useParams()

  useEffect(() => {
    if (id)
      getPangolin(token, id).then((response) => {
        setPangolin(response)
      })
  }, [id])

  return (
    <Card>
      {pangolin && (
        <Descriptions title={`Pangolin ${id}`} bordered size="small" style={{ margin: 20 }}>
          <Descriptions.Item label="Pangolearn version">
            {pangolin[0]?.pangolin?.pangolearn_version}
          </Descriptions.Item>
          <Descriptions.Item label="Lineage information">
            <a href={`https://cov-lineages.org/lineage.html?lineage=${id}`}>{id}</a>
          </Descriptions.Item>
        </Descriptions>
      )}

      <SamplesTable samples={pangolin} />
    </Card>
  )
}

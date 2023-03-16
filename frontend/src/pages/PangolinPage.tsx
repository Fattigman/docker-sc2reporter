import React, { useEffect, useState } from 'react'
import { Card } from 'antd'
import { SamplesTable } from 'components/SamplesTable'
import { useParams } from 'react-router-dom'
import { getPangolin } from 'services/api'

export const PangolinPage = ({ token, isAdmin }) => {
  const [samples, setSamples] = useState<any>()
  const [refresh, setRefresh] = useState<boolean>(false)
  const [isLoading, setIsLoading] = useState<boolean>(true)
  const { id } = useParams()
  const title = `Pangolin ${id}`
  const covLineagesLink = `https://cov-lineages.org/lineage.html?lineage=${id}`

  useEffect(() => {
    if (id)
      getPangolin(token, id)
        .then((response) => {
          setSamples(response.samples)
          setIsLoading(false)
        })
        .catch(() => setIsLoading(false))
  }, [id, refresh])

  const refreshSamples = () => {
    setRefresh((prevRefresh) => !prevRefresh)
  }

  return (
    <Card>
      <SamplesTable
        token={token}
        samples={samples}
        refreshSamples={refreshSamples}
        isAdmin={isAdmin}
        title={title}
        subTitle={<a href={covLineagesLink}>Lineage information</a>}
        loading={isLoading}
      />
    </Card>
  )
}

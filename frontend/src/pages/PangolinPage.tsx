import React, { useEffect, useState } from 'react'
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
    <SamplesTable
      samples={pangolin}
      title={'Pangolin'}
      subTitle={
        <a href={`https://cov-lineages.org/lineage.html?lineage=${id}`}>Lineage information</a>
      }
    />
  )
}

import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { getNextclade } from '../services/api'
import { SamplesTable } from '../components/SamplesTable'

export const NextcladePage = ({ token }) => {
  const [samples, setSamples] = useState<any>()
  const { id } = useParams()

  useEffect(() => {
    if (id)
      getNextclade(token, id).then((response) => {
        setSamples(response)
      })
  }, [id])

  return <SamplesTable samples={samples} title={'Nextclade'} subTitle={null} />
}

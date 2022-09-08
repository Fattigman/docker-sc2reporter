import React from 'react'
import { useParams } from 'react-router-dom'
import { Result } from 'antd'

export const SamplePage = ({ samples }) => {
  const { id } = useParams()
  const sample = samples.filter((sample) => sample.sample_id === id)[0]
  return sample ? (
    <div>Sample page</div>
  ) : (
    <Result status="404" title="404" subTitle="Sorry, the page you visited does not exist." />
  )
}

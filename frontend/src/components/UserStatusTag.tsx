import React from 'react'
import { Tag } from 'antd'

export const UserStatusTag = ({ isDisabled }) =>
  isDisabled ? <Tag color={'gray'}>disabled</Tag> : <Tag color={'green'}>enabled</Tag>

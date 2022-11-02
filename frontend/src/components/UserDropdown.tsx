import React from 'react'
import { Button, Dropdown, Popover, Space, Tag } from 'antd'
import { DownOutlined } from '@ant-design/icons'
import { scopes } from '../services/costants'
import { UserStatusTag } from './UserStatusTag'

export const UserDropdown = ({ user }) => {
  const { email, username, fullname, scope, disabled } = user
  return (
    <Popover
      placement="bottom"
      title={<>{fullname}</>}
      content={
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start', gap: 5 }}>
          <>{email}</>
          <Tag color={scopes[scope].color}>{scope}</Tag>
          <UserStatusTag isDisabled={disabled} />
        </div>
      }
      trigger="hover"
    >
      {username} <DownOutlined />
    </Popover>
  )
}

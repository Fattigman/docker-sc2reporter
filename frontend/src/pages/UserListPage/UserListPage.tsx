import React, { useEffect, useState } from 'react'
import { notification, Popconfirm, Result, Table, Tag, Tooltip } from 'antd'
import { DeleteTwoTone } from '@ant-design/icons'
import { deleteUser, getUsers } from '../../services/api'
import { NewUserModal } from '../../components/NewUserModal'
import { LoadingPage } from '../LoadingPage'
import { scopes } from '../../services/costants'
import { UserStatusTag } from '../../components/UserStatusTag'

export const UserListPage = ({ token }) => {
  const [users, setUsers] = useState<any[]>()
  const [isLoading, setIsLoading] = useState<boolean>(true)

  useEffect(() => {
    updateUsersList()
  }, [])

  const updateUsersList = () => {
    getUsers(token)
      .then((response) => {
        setUsers(response)
        setIsLoading(false)
      })
      .catch(() => setIsLoading(false))
  }

  const confirmDeleteUser = (token: string, username: string) => {
    deleteUser(token, username).then(() => {
      notification['success']({
        message: `User ${username} deleted`,
      })
      getUsers(token)
        .then((users) => {
          setUsers(users)
          setIsLoading(false)
        })
        .catch(() => {
          setIsLoading(false)
        })
    })
  }

  const columns = [
    {
      title: 'Username',
      dataIndex: 'username',
      key: 'username',
    },
    {
      title: 'Full Name',
      dataIndex: 'fullname',
      key: 'fullname',
    },
    {
      title: 'Email',
      dataIndex: 'email',
      key: 'email',
    },
    {
      title: 'Status',
      dataIndex: 'disabled',
      key: 'disabled',
      render: ({ disabled }) => <UserStatusTag isDisabled={disabled} />,
    },
    {
      title: 'Scope',
      key: 'scope',
      render: ({ scope }) => <Tag color={scopes[scope].color}>{scope}</Tag>,
    },
    {
      title: 'Actions',
      key: 'actions',
      render: ({ username }) => (
        <div style={{ display: 'flex' }}>
          <Tooltip title="Delete user">
            <Popconfirm
              title="Are you sure you want to delete this user?"
              onConfirm={() => confirmDeleteUser(token, username)}
              okText="Yes"
              cancelText="No"
            >
              <DeleteTwoTone style={{ fontSize: '20px' }} />
            </Popconfirm>
          </Tooltip>
        </div>
      ),
    },
  ]

  return (
    <div>
      {isLoading ? (
        <LoadingPage />
      ) : (
        <>
          {users ? (
            <Table
              dataSource={users}
              columns={columns}
              pagination={false}
              rowKey={({ email }) => email}
              tableLayout={'fixed'}
              title={() => (
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <NewUserModal updateUsers={updateUsersList} token={token} />
                </div>
              )}
            />
          ) : (
            <Result status="error" subTitle="Sorry, something went wrong." />
          )}
        </>
      )}
    </div>
  )
}

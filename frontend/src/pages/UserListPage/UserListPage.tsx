import React, { useEffect, useState } from 'react'
import { notification, Popconfirm, Table, Tag, Tooltip } from 'antd'
import { DeleteTwoTone } from '@ant-design/icons'
import { deleteUser, getUsers } from '../../services/api'
import { NewUserModal } from '../../components/NewUserModal'
import { LoadingPage } from '../LoadingPage'

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

  const confirmDeleteUser = (tolken: string, username: string) => {
    deleteUser(token, username).then(() => {
      notification['success']({
        message: `User deleted`,
      })
      getUsers(token).then((users) => {
        setUsers(users)
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
      title: 'Disabled',
      dataIndex: 'disabled',
      key: 'disabled',
    },
    {
      title: 'scope',
      key: 'scope',
      render: ({ scope }) => {
        return scope
      },
    },
    {
      title: 'Actions',
      key: 'actions',
      render: ({ username, email }) => (
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
          {users && (
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
          )}
        </>
      )}
    </div>
  )
}

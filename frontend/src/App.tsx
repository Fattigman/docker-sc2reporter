import React, { useState } from 'react'
import styles from './App.module.css'
import { Button, Layout, Menu } from 'antd'
import { Link, Route, Routes, useLocation } from 'react-router-dom'
import { SamplesTable } from './components/SamplesTable'
import { LoginPage } from './pages/Login/LoginPage'
import { getSamples, getToken } from './services/api'
import { SamplePage } from './pages/SamplePage'
import { LoadingPage } from './pages/LoadingPage'
import { NextcladePage } from './pages/NextcladePage'

const { Header, Content } = Layout
export const App = () => {
  const [user, setUser] = useState<any>()
  const [samples, setSamples] = useState<any>()
  const [token, setToken] = useState<any>()

  const menuItems = [
    {
      key: 'Home',
      label: <Link to="/">Home</Link>,
    },
  ]

  const login = (formInput) => {
    getToken(formInput).then((response) => {
      setToken(response.access_token)
      setUser(formInput.username)
      getSamples(response.access_token).then((samples) => setSamples(samples))
    })
  }

  const logout = () => {
    setToken(null)
    setUser(null)
  }

  return (
    <div className="app">
      <Layout style={{ minHeight: '100vh' }}>
        <Header className={styles.header}>
          <Menu
            theme="dark"
            mode="horizontal"
            defaultSelectedKeys={['home']}
            selectedKeys={[useLocation().pathname.split('/')[1]]}
            style={{ width: '72%' }}
            items={menuItems}
          />
          <div className={styles.logout}>
            <div className={styles.username}>{user}</div>
            <div>
              {token && (
                <Button type="primary" onClick={() => logout()}>
                  Logout
                </Button>
              )}
            </div>
          </div>
        </Header>
        <Content
          className={styles.siteLayout}
          style={{
            padding: '0 50px',
            marginTop: 64,
            minHeight: 'calc(100vh - 155px)',
          }}
        >
          <Routes>
            <Route
              path="/"
              element={token ? <SamplesTable samples={samples} /> : <LoginPage login={login} />}
            />
            <Route
              path="/samples/:id"
              element={
                token ? (
                  samples ? (
                    <SamplePage samples={samples} />
                  ) : (
                    <LoadingPage />
                  )
                ) : (
                  <LoginPage login={login} />
                )
              }
            />
            <Route
              path="/nextclade/:id"
              element={token ? <NextcladePage token={token} /> : <LoginPage login={login} />}
            />
          </Routes>
        </Content>
        <footer data-testid="footer" className={styles.footer}>
          <a href={'https://www.scilifelab.se/units/clinical-genomics/'}>Clinical Genomics</a>
        </footer>
      </Layout>
    </div>
  )
}

import React, { useEffect, useState } from 'react'
import styles from './App.module.css'
import { Button, Layout, Menu } from 'antd'
import { Link, Route, Routes, useLocation } from 'react-router-dom'
import { LoginPage } from './pages/Login/LoginPage'
import { getSamples, getToken, getUserInfo } from './services/api'
import { SamplePage } from './pages/SamplePage'
import { LoadingPage } from './pages/LoadingPage'
import { VariantPage } from './pages/VariantPage'
import { NextcladePage } from './pages/NextcladePage'
import { PangolinPage } from 'pages/PangolinPage'
import { SamplesPage } from 'pages/SamplesPage'
import { UserListPage } from './pages/UserListPage/UserListPage'
import { UserDropdown } from './components/UserDropdown'
import jwt_decode from 'jwt-decode'
import moment from 'moment'
import { DashboardPage } from './pages/DashboardPage'
import { scopes } from './services/costants'

const { Header, Content } = Layout
export const App = () => {
  const [user, setUser] = useState<any>()
  const [isAdmin, setIsAdmin] = useState<boolean>(false)
  const [samples, setSamples] = useState<any>()
  const [token, setToken] = useState<any>(null)
  const tokenCookieName = 'sc2reporterToken'
  const findCookiePattern = new RegExp(`(?<=${tokenCookieName}=)(.*)(?=;)`, 'g')
  const cookieAge = 10 // hours
  const currentTime = moment().unix()

  const menuItems = [
    {
      key: '',
      label: <Link to="/">Home</Link>,
      disabled: token === null,
      hide: 'false',
    },
    {
      key: 'dashboard',
      label: <Link to="/dashboard">Dashboard</Link>,
      disabled: token === null,
      hide: 'false',
    },
    {
      key: 'users',
      label: <Link to="/users">Users</Link>,
      hide: (!isAdmin).toString(),
    },
  ].filter((item) => item.hide === 'false')

  useEffect(() => {
    const cookieToken = `${document.cookie};`.match(findCookiePattern)
    if (cookieToken?.length === 1) {
      setToken(cookieToken[0])
      getUserInfo(cookieToken[0]).then((response) => setUser(response))
      getSamples(cookieToken[0]).then((samples) => setSamples(samples))
    }
  }, [])

  useEffect(() => {
    if (user?.scope === scopes.admin.id) setIsAdmin(true)
    else setIsAdmin(false)
  }, [user])

  const login = (formInput) => {
    getToken(formInput).then((response) => {
      setToken(response.access_token)
      getUserInfo(response.access_token).then((response) => setUser(response))
      getSamples(response.access_token).then((samples) => setSamples(samples))
      document.cookie = `${tokenCookieName}=${response.access_token}; Max-Age=${
        cookieAge * 60 * 60
      };`
    })
  }

  const logout = () => {
    setToken(null)
    setUser(null)
    document.cookie = `${tokenCookieName}=; Max-Age=0;`
  }

  if (token) {
    const decoded = jwt_decode(token) as any
    if (decoded?.exp < currentTime) {
      logout()
    }
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
            {user && (
              <div className={styles.username}>
                <UserDropdown user={user} />
              </div>
            )}
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
              element={
                token ? (
                  <SamplesPage token={token} isAdmin={isAdmin} />
                ) : (
                  <LoginPage login={login} />
                )
              }
            />
            <Route
              path="/dashboard"
              element={token ? <DashboardPage token={token} /> : <LoginPage login={login} />}
            />
            <Route
              path="/samples/:id"
              element={
                token ? (
                  samples ? (
                    <SamplePage token={token} />
                  ) : (
                    <LoadingPage />
                  )
                ) : (
                  <LoginPage login={login} />
                )
              }
            />
            <Route
              path="/users"
              element={token ? <UserListPage token={token} /> : <LoginPage login={login} />}
            />
            <Route
              path="/nextclade/:id"
              element={
                token ? (
                  <NextcladePage token={token} isAdmin={isAdmin} />
                ) : (
                  <LoginPage login={login} />
                )
              }
            />
            <Route
              path="/pangolin/:id"
              element={
                token ? (
                  <PangolinPage token={token} isAdmin={isAdmin} />
                ) : (
                  <LoginPage login={login} />
                )
              }
            />
            <Route
              path="/variants/:id"
              element={token ? <VariantPage token={token} /> : <LoginPage login={login} />}
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

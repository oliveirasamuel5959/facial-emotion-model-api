import React from 'react'
import Users from './Users'
import { NavLink } from 'react-router-dom'

const Admin = () => {
  return (
    <section>
        <h1>Admin Page</h1>
        <br />
        <Users />
        <br />
        <div className='flex-grow'>
            <NavLink to="/home" >Home</NavLink>
        </div>
    </section>
  )
}

export default Admin;

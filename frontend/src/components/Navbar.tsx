import { Link, NavLink } from 'react-router-dom'
import './navbar.css'

const Navbar = () => {
    return (
        <nav className="nav">
            <Link to="/home" className="site_title">FER</Link>
            <ul>
                <li>
                    <NavLink to="/login" >Login</NavLink>
                </li>
                <li>
                    <NavLink to="/stream" >Stream</NavLink>
                </li>
                <li>
                    <NavLink to="/image" >Picture</NavLink>
                </li>
            </ul>
        </nav>
    )
}

export default Navbar
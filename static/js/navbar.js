var NavBar = React.createClass({
    render: function() {
        const orange_background = {
            backgroundColor: 'orange'
        };
        const white_color = {
            color: 'white'
        };
        const logo_size = {
            width: '60px', height: 'auto'
        };
        var login_logout;
        if (Boolean(data.user_id)) {
            login_logout = (
                <ul className="dropdown menu" style={orange_background} data-dropdown-menu>
                    <li><a href="#">Program Tour</a></li>
                    <li><a href="#">Item1</a></li>
                    <li><a href="#">Item1</a></li>
                    <li><a href="/profile">View Profile</a></li>
                    <li><a href="/logout">Logout</a></li>
                </ul>
            );
        }
        else {
            login_logout = (
                <ul className="dropdown menu" style={orange_background} data-dropdown-menu>
                    <li><a href="#">Program Tour</a></li>
                    <li><a href="#">Item1</a></li>
                    <li><a href="#">Item1</a></li>
                <li><a href="/register">Register</a></li>
                <li><a href="/login">Login</a></li>
                </ul>
            );
        }
        return (
        <div className="fixed hide-for-small contain-to-grid">
        <nav className="top-bar" style={orange_background} role="navigation">
            <div className="top-bar-left align-self-middle">
                <div className="section-background" style={white_color}>
                        <a href="/">
                            <img src={data.logo} alt="" style={logo_size} />
                            Trip Finder
                        </a>
                </div>
            </div>
            <div className="top-bar-right">
                {login_logout}
            </div>
        </nav>
        </div>
        );
    }
});

ReactDOM.render(
    React.createElement(NavBar, {}),
    document.getElementById("navbar")
);

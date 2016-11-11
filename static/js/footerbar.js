var FooterBar = React.createClass({
    render: function() {
        var footerStyle = {
            backgroundColor: 'orange',
            padding: '7px'
        };
        var imgStyle = {
            width: '60px',
            height: 'auto'
        };
        return (<footer className="footer" style={footerStyle}>
                <img style={imgStyle} src={data.logo} />
            <div className="top-bar-right align-self-middle">
                <a href="/aboutus/">About us</a>
            </div>
        </footer>);
    }
});

ReactDOM.render(
    React.createElement(FooterBar, {}),
    document.getElementById('footer-bar')
);

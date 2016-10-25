var FooterBar = React.createClass({
    render: function() {
        var footerStyle = {
            backgroundColor: 'orange'
        };
        var imgStyle = {
            width: '60px',
            height: 'auto'
        };
        return (<footer className="footer" style={footerStyle} >
            <img style={imgStyle} src={data.logo} />
        </footer>);
    }
});

ReactDOM.render(
    React.createElement(FooterBar, {}),
    document.getElementById('footer-bar')
);

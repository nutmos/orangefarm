var NavBar = React.createClass({
    render: function() {
        var rows = [];
        var active = this.state.active;
        for (var i = 0; i < 4; ++i) {
            if (i === active) {
                rows.push((<li class="active"><a href="#">item 1</a></li>));
            }
            else {
                rows.push(<li><a href="#">item 1</a></li>);
            }
        }
        return (
        <nav class="top-bar" style="background-color: orange;" role="navigation">
            <div class="top-bar-left">
                <div class="section-background" style="color: white; font-size: 30px">
                        Trip Finder
                </div>
            </div>
            <div class="top-bar-right">
                <ul class="dropdown menu section-background" style="background-color: orange;" data-dropdown-menu>
                    {rows}
                </ul>
            </div>
        </nav>
        );
    }
});

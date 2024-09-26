<h1 style="text-align: center;">Constraint Satisfaction Problem (AI)</h1>
<p>This is a proof of concept project meant to solve a csp problem without the use of existing libraries such as <a href="https://github.com/python-constraint/python-constraint">python-constraint</a>.</p>
<img src= "screenshots\screenshot1.png">
<h2>Content</h2>
<ul>
    <li><a href = "#goal">Goal</a></li>
    <li><a href = "#usage">Usage</a></li><ul>
    <li><a href = "#source">From Source</a></li>
    </ul>
    <li><a href = "#issues">Issues</a></li>
</ul>

<h2 id = "goal">Goal</h2>
<p>Suppouse we have a set of sensors and tragets we want to identify as many targets as possible at given time while satisfying the following constraints: 1-Each sensor can only focus on 1 target at a time. 2-Three sensors are required to identify a target's position.<br>*note that sensors have a given range.</p>
<p>This is achived using two matrices. One for determining which sensors are in each other's range and can communicate and another one for determining which targets are in which sensors effective range. then using these two matrices we generate a tree and navigate it with a dfs approach.</p>
<h2 id = "usage">Usage</h2>
<h3 id = "source">From Source</h3>
<p>Make sure you have Python and required libraries installed and run <code>python gui.py</code>.</p>
<h2 id = "issues">Issues</h2>
<p>Please refer to issues tab to see a list of current identified issues or to to submit your own.</p>
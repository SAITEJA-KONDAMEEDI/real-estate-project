
with open('app.py', 'r') as f:

    content = f.read()



old = '''            <select id="mandal" onchange="loadInfo()" disabled>

                <option value="">-- Select Mandal --</option>

            </select>

        </div>

    </div>



    <div id="result">'''



new = '''            <select id="mandal" onchange="loadInfo()" disabled>

                <option value="">-- Select Mandal --</option>

            </select>

        </div>

        <div class="info-stat-block">

            <div class="stat-item">

                <span class="stat-number">51</span>

                <span class="stat-label">Locations Covered</span>

            </div>

            <div class="stat-item">

                <span class="stat-number">2</span>

                <span class="stat-label">States Tracked</span>

            </div>

            <div class="stat-item">

                <span class="stat-number">Live</span>

                <span class="stat-label">Azure MySQL Data</span>

            </div>

        </div>

    </div>



    <div id="result">'''



if old not in content:

    print("ERROR: old block not found — no changes made")

else:

    content = content.replace(old, new, 1)

    with open('app.py', 'w') as f:

        f.write(content)

    print("SUCCESS: stat block inserted")


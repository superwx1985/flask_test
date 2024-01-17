from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, Response
)
import json

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/add', methods=('GET',))
def add():
    if request.method == 'GET':
        a = int(request.args.get("a", 0))
        b = int(request.args.get("b", 0))
        return {"input": f"{a}+{b}", "result": a+b, "debug": None}


@bp.route('/json', methods=('GET',))
def _json():
    if request.method == 'GET':
        json_str = """
{
"lotto":{
 "lottoId":5,
 "winning-numbers":[2,45,34,23,7,5,3],
 "winners":[{
   "winnerId":23,
   "numbers":[2,45,34,23,3,5]
 },{
   "winnerId":54,
   "numbers":[52,3,12,11,18,22]
 }]
}
}
        """

        return json.loads(json_str)


@bp.route('/xpath', methods=('GET',))
def _xpath():
    if request.method == 'GET':
        xpath_str = """
<shopping>
      <category type="groceries">
        <item>Chocolate</item>
        <item quantity="99">Coffee</item>
      </category>
      <category type="supplies">
        <item>Paper</item>
        <item quantity="4">Pens</item>
      </category>
      <category type="supplies2">
        <item>Paper</item>
        <item quantity="222">Pens</item>
      </category>
      <category type="present">
        <item when="Aug 10">Kathryn's Birthday</item>
      </category>
</shopping>
        """
        return Response(response=xpath_str, content_type="application/xml")

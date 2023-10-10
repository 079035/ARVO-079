# Get Embeding Vector from CVEFixes
- Download the dababase 
- Grab the simple fixes (1 file and 1 modification): 1111 CVEs
- Get the vul code of CVEs
    - Clone
    - Diff
    - Extract Vul code
- Store the Vector of the vul code

TODO:
- Get more detailed vul code(longer)

## Embeding Token Limit
```
CVE-2018-10821:
openai.error.InvalidRequestError: This model's maximum context length is 8191 tokens, however you requested 9395 tokens (9395 in your prompt; 0 for the completion). Please reduce your prompt; or completion length.
```

Just one case in 1111 cases. I jut ignore it.

```
 */
 function getMethods(a){var b=[],c;for(c in a)try{"function"==typeof a[c]&&b.push(c+": "+a[c].toString())}catch(e){b.push(c+": inaccessible")}return b}function dump(a,b){var c="";b||(b=0);for(var e="",d=0;d<b+1;d++)e+=" ";if("object"==typeof a)for(var f in a)d=a[f],"object"==typeof d?(c+=e+"'"+f+"' ...\n",c+=dump(d,b+1)):c+=e+"'"+f+"' => \""+d+'"\n';else c="===>"+a+"<===("+typeof a+")";return c};(function(a){a.fn.fc_set_tab_list=function(b){var c={toggle_speed:300,fc_list_forms:a(".fc_list_forms"),fc_list_add:a("#fc_list_add")};b=a.extend(c,b);return this.each(function(){var c=a(this),d=c.closest("
...
```

# CWE Vul Code

- Parse the xml file

Todo:
- Get the vectors


# Find Most Similar CVE Vul Code
- Compute the similarity of the Vul Code and the CVE code
- Get the most similar one

## Issues

- Does it work?
    - For example, if I write an UAF, it can't return a CVE related to UAF.
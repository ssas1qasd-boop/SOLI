# Replace named destinations in internal links with explicit [page /XYZ left top 0] targets
# (many phone PDF viewers ignore named destinations).
import sys
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, NameObject, NumberObject, FloatObject, NullObject, DictionaryObject

def fix(path):
    r = PdfReader(path)
    w = PdfWriter(clone_from=r)
    nd = w._get_named_destinations() if hasattr(w, '_get_named_destinations') else None
    nd = r.named_destinations
    page_ids = {id(p.indirect_reference.idnum if hasattr(p, 'indirect_reference') else p): i for i, p in enumerate(r.pages)}
    # map page index from reader destination
    def target(name):
        d = nd.get(name)
        if d is None: return None
        pidx = r.get_destination_page_number(d)
        top = d.top if d.top is not None else 0
        left = d.left if d.left is not None else 0
        return ArrayObject([w.pages[pidx].indirect_reference, NameObject('/XYZ'), FloatObject(left), FloatObject(top), NumberObject(0)])
    n = 0
    for page in w.pages:
        if '/Annots' in page:
            keep = [a for a in page['/Annots'] if not (a.get_object().get('/Subtype') == '/Link' and a.get_object().get('/A') is not None
                    and str(a.get_object()['/A'].get_object().get('/URI', '')).startswith('file:'))]
            page[NameObject('/Annots')] = ArrayObject(keep)
        for a in page.get('/Annots') or []:
            a = a.get_object()
            if a.get('/Subtype') != '/Link': continue
            dest = a.get('/Dest')
            act = a.get('/A')
            if act is not None and act.get_object().get('/URI') == 'https://goback.invalid/':
                a[NameObject('/A')] = DictionaryObject({NameObject('/S'): NameObject('/Named'), NameObject('/N'): NameObject('/GoBack')})
                n += 1
                continue
            name = None
            if isinstance(dest, str): name = dest
            elif act is not None and act.get('/S') == '/GoTo' and isinstance(act.get('/D'), str): name = act.get('/D')
            if name is None: continue
            t = target(name)
            if t is None: continue
            if '/A' in a: del a[NameObject('/A')]
            a[NameObject('/Dest')] = t
            n += 1
    w.write(path)
    return n

if __name__ == '__main__':
    for p in sys.argv[1:]:
        print(p, fix(p), 'links fixed')

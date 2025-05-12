/* mod_source_port.c - Add source port format string */
#include "httpd.h"
#include "http_config.h"
#include "http_protocol.h"
#include "http_log.h"
#include "ap_config.h"
#include "util_filter.h"
#include "apr_strings.h"
#include "apr_lib.h"

static int sourceport_header_parser(request_rec *r)
{
    conn_rec *c = r->connection;
    apr_port_t port = c->client_addr->port;
    char port_str[20];
    
    sprintf(port_str, "%u", port);
    apr_table_setn(r->notes, "sourceport", apr_pstrdup(r->pool, port_str));
    return DECLINED;
}

static const char *log_sourceport(request_rec *r, char *a)
{
    return apr_table_get(r->notes, "sourceport");
}

static void register_hooks(apr_pool_t *p)
{
    ap_hook_header_parser(sourceport_header_parser, NULL, NULL, APR_HOOK_MIDDLE);
    ap_register_output_filter("SOURCEPORT", log_sourceport, NULL, AP_FTYPE_RESOURCE);
}

static const command_rec sourceport_cmds[] = {
    { NULL }
};

module AP_MODULE_DECLARE_DATA source_port_module = {
    STANDARD20_MODULE_STUFF,
    NULL,                   /* create per-dir config */
    NULL,                   /* merge per-dir config */
    NULL,                   /* create per-server config */
    NULL,                   /* merge per-server config */
    sourceport_cmds,        /* command table */
    register_hooks          /* register hooks */
};